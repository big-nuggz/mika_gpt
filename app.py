import os

from datetime import datetime

import subprocess

from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import json
import uuid

# Hello chatgpt, I'm calling you from within Python using your API!
API_KEY_PATH = './apikey.txt'
CONVERSATION_HISTORY_PATH = './chats'
SYSTEM_PROMPT_PATH = './system_prompt.json'
TITLE_PROMPT_PATH = './title_prompt.json'

# tts stuff
PIPER_PATH = './piper/piper.exe'
VOICE_PATH = './voices/en_US_libritts_r_medium_en_US-libritts_r-medium.onnx'
TTS_OUT_PATH = './voice.ogg'


with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf8') as f:
    system_prompt = json.load(f)

with open(TITLE_PROMPT_PATH, 'r', encoding='utf8') as f:
    title_prompt = json.load(f)

with open(API_KEY_PATH, 'r', encoding='utf8') as f:
    api_key = f.readline()

os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

app = Flask(__name__)


def get_unix_time():
    return round(datetime.now().timestamp())

def save_conversation_data(history: list, file_path: str) -> None:
    with open(file_path, 'w', encoding='utf8') as f:
        json.dump(history, f)

def load_conversation_data(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf8') as f:
            return json.load(f)
    except FileNotFoundError:
        return create_new_conversation_data()
    
def create_title(user_prompt, model):
    completion = client.chat.completions.create(
        model=model, 
        messages=[title_prompt] + user_prompt
    )

    title = completion.choices[0].message.content
    return title

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def create_new_conversation_data():
    conversation_data = {
        "uuid": str(uuid.uuid4()),
        "title": "", 
        "created": str(get_unix_time()), 
        "contexts": [], 
        "current_conversation": [],
        "full_history": [] 
    }
    return conversation_data

def print_statistics(usage):
    print(f'tokens in the generated completion: {usage.completion_tokens}')
    print(f'tokens in the prompt: {usage.prompt_tokens}')
    print(f'total tokens used in the request: {usage.total_tokens}')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/create', methods=['GET'])
def init_conversation():
    conversation_data = create_new_conversation_data();

    return jsonify(conversation_data)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json

    file_name = data['uuid'] + '.json'

    conversation_data = load_conversation_data(os.path.join(CONVERSATION_HISTORY_PATH, file_name))

    # if they're different, that means load failed and function returned a new empty conversation
    if data['uuid'] != conversation_data['uuid']:
        conversation_data['uuid'] = data['uuid']

    conversation_data['full_history'].extend(data['messages'])
    conversation_data['current_conversation'].extend(data['messages'])

    if conversation_data['title'] == '':
        conversation_data['title'] = create_title(data['messages'], data['model'])

    completion = client.chat.completions.create(
        model=data['model'], 
        messages=[system_prompt] + conversation_data['full_history']
    )

    reply = completion.choices[0].message.content

    print_statistics(completion.usage)

    conversation_data['full_history'].append({
            'role': 'assistant', 'content': reply
    })
    conversation_data['current_conversation'].append({
            'role': 'assistant', 'content': reply
    })

    # TODO: add way to compress current conversation

    save_conversation_data(conversation_data, os.path.join(CONVERSATION_HISTORY_PATH, file_name))

    return jsonify(reply)

@app.route('/api/history', methods=['POST'])
def get_history():
    data = request.json
    file_name = data['uuid'] + '.json'
    conversation_data = load_conversation_data(os.path.join(CONVERSATION_HISTORY_PATH, file_name))

    return jsonify(conversation_data['full_history'])

@app.route('/api/convlist', methods=['GET'])
def get_conversation_list():
    file_list = os.listdir(CONVERSATION_HISTORY_PATH)
    
    data_list = []
    for file in file_list:
        file_path = os.path.join(CONVERSATION_HISTORY_PATH, file)
        data = load_conversation_data(file_path)
        data_list.append({
            "uuid": data['uuid'], 
            "title": data['title'], 
            "created": data['created'], 
            "last_edited": str(round(os.path.getmtime(file_path)))
        })

    data_list = sorted(data_list, key=lambda x: x['last_edited'], reverse=True)

    return jsonify(data_list)

@app.route('/api/delete', methods=['POST'])
def delete_conversation():
    data = request.json
    file_name = data['uuid'] + '.json'

    delete_file(os.path.join(CONVERSATION_HISTORY_PATH, file_name))
    return jsonify({'status': 'success'})

@app.route('/api/tts', methods=['POST'])
def speak_text():
    data = request.json
    text = data['text']

    command = f'{PIPER_PATH} -m {VOICE_PATH} -f {TTS_OUT_PATH}'
    subprocess.run(command, input=str.encode(text))

    return send_file(TTS_OUT_PATH, mimetype='audio/ogg', download_name='voice.ogg')

if __name__ == '__main__':
    app.run(debug=True)