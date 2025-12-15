import re

from ..constants import CORE_MEMORY_UPDATE_PROMPT_SEARCH_STRING


def find_core_memory_update_prompt(response: str) -> str:
    ''' 
    checks if response message contains special core update image prompt string or not
    if yes, returns the prompt string
    if no, returns None
    '''
    r = re.search(CORE_MEMORY_UPDATE_PROMPT_SEARCH_STRING, response, re.DOTALL)
    if r:
        return r.group(1)
    
    return None


def strip_core_memory_update_prompt(response: str) -> str:
    ''' 
    removes core memory update prompt from original response and returns stripped version
    '''
    return re.sub(CORE_MEMORY_UPDATE_PROMPT_SEARCH_STRING, '', response, flags=re.DOTALL)