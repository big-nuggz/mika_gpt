import os
import subprocess

from flask import Flask, render_template, request, jsonify, send_file

from openai import OpenAI

from api.file import *
from api.constants import *
from api.conversation import *
from api.data import *
from api.image import *
from api.tokens import get_token_count_from_chat


system_prompt = load_json(SYSTEM_PROMPT_PATH)
title_prompt = load_json(TITLE_PROMPT_PATH)
compression_prompt = load_json(COMPRESSION_PROMPT_PATH)

if SUPPLIER == 'OPENAI':
    client = OpenAI(
        api_key = load_api_key(API_KEY_PATH_OPENAI)
    )
elif SUPPLIER == 'GOOGLE':
    client = OpenAI(
        api_key = load_api_key(API_KEY_PATH_GOOGLE), 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/create', methods=['GET'])
def init_conversation():
    conversation_data = create_new_conversation_data()

    return jsonify(conversation_data)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json

    file_name = data['uuid'] + '.json'

    conversation_data = load_conversation_data(os.path.join(CONVERSATION_HISTORY_PATH, file_name))

    # if they're different, that means load failed and function returned a new empty conversation
    if data['uuid'] != conversation_data['uuid']:
        conversation_data['uuid'] = data['uuid']

    if conversation_data['title'] == '':
        conversation_data['title'] = create_title(client, data['messages'], title_prompt, MODEL_TITLING)

    # if convo contains image, use model with vision, otherwise use most intelligent text-only model
    response_model = MODEL_VISION
    if has_image(conversation_data):
        # response_model = MODEL_VISION
        print('this conversation contains image(s)')
    else:
        response_model = MODEL_NON_VISION

    print(f'using {response_model} to respond')

    # if context is too long, compress it
    current_token_count = get_token_count_from_chat(conversation_data['current_conversation'], TOKEN_ENCODER) 
    if current_token_count >= TOKEN_COMPRESSION_LIMIT:
        print(f'token limit exceeded. tokens: {current_token_count}')
        print(f'compressing...')

        # compression
        completion = client.chat.completions.create(
            model=response_model, 
            messages=conversation_data['current_conversation'] + [compression_prompt])
        
        reply = completion.choices[0].message.content

        conversation_data['current_conversation'] = [{
                'role': 'assistant', 'content': reply
        }]

        current_token_count = get_token_count_from_chat(conversation_data['current_conversation'], TOKEN_ENCODER) 
        print(f'token count after compression: {current_token_count}')

    # reply
    conversation_data['full_history'].extend(data['messages'])
    conversation_data['current_conversation'].extend(data['messages'])

    completion = client.chat.completions.create(
        model=response_model, 
        messages=[system_prompt] + conversation_data['current_conversation']
    )

    reply = completion.choices[0].message.content

    print_statistics(completion.usage)

    conversation_data['full_history'].append({
        'role': 'assistant', 'content': reply
    })

    # image generation
    image_prompt = find_image_prompt(reply)
    if image_prompt:
        print('image generation triggered')
        b64_image = generate_image(client, DALLE_MODEL, image_prompt, size=IMAGE_RESOLUTION)
        image_reply = [
                        {
                            'type': 'text', 
                            'text': strip_image_prompt(reply)
                        }, 
                        {
                            "type": "image_url", 
                            "image_url": {"url": 'data:image/png;base64,' + b64_image}, 
                            # 'prompt': image_prompt
                        }
                      ]
        
        conversation_data['current_conversation'].append({
            'role': 'assistant', 'content': image_reply
        })
        conversation_data['full_history'].append({
            'role': 'assistant', 'content': image_reply
        })
    else: 
        conversation_data['current_conversation'].append({
                'role': 'assistant', 'content': reply
        })

    save_json(conversation_data, os.path.join(CONVERSATION_HISTORY_PATH, file_name))

    if image_prompt:
        return jsonify(image_reply)
    else:
        return jsonify(reply)

@app.route('/api/history', methods=['POST'])
def get_history():
    data = request.json
    file_name = data['uuid'] + '.json'
    conversation_data = load_conversation_data(os.path.join(CONVERSATION_HISTORY_PATH, file_name))

    return jsonify(conversation_data['current_conversation'])

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