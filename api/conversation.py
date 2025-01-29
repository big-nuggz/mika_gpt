import uuid

from .file import load_json
from .data import get_unix_time

from openai import OpenAI

def create_title(client: OpenAI, user_prompt: dict, title_prompt: dict, model: str) -> str:
    ''' returns a title of the conversation based on given prompt '''
    completion = client.chat.completions.create(
        model=model, 
        messages=[title_prompt] + user_prompt
    )

    title = completion.choices[0].message.content
    return title

def load_conversation_data(file_path: str) -> list:
    ''' 
    if file exists, returns content 
    otherwise return new empty conversation
    '''
    try:
        return load_json(file_path)
    except FileNotFoundError:
        return create_new_conversation_data()
    
def create_new_conversation_data() -> dict:
    ''' creates new empty conversation '''
    conversation_data = {
        "uuid": str(uuid.uuid4()),
        "title": "", 
        "created": str(get_unix_time()), 
        "contexts": [], 
        "current_conversation": [],
        "full_history": [] 
    }
    return conversation_data