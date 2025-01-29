import re

from openai import OpenAI

from .constants import IMAGE_PROMPT_SEARCH_STRING

def generate_image(client: OpenAI, model: str, prompt: str, size='512x512', quality='standard'):
    ''' return b64 encoded image '''
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        response_format='b64_json', 
        n=1,
    )

    return response.data[0].b64_json

def find_image_prompt(response: str) -> str:
    ''' 
    checks if response message contains special image prompt string or not
    if yes, returns the prompt string
    if no, returns None
    '''
    r = re.search(IMAGE_PROMPT_SEARCH_STRING, response)
    if r:
        return r.group(1)
    
    return None

def strip_image_prompt(response: str) -> str:
    ''' 
    removes image generation prompt from original response and returns stripped version
    '''
    return re.sub(IMAGE_PROMPT_SEARCH_STRING, '', response)