import re
import time
import json
import subprocess
import sys

from ..constants import CORE_MEMORY_UPDATE_PROMPT_SEARCH_STRING, BATCH_MEMORY_WORKER_PATH


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


def save_batch_memory(memories: str, conversation_id: str, path: str) -> None:
    '''
    dump extracted memories into a json, which the worker will used to update the memory entries later on
    
    :param memories: multi-line string of memories
    :type memories: str
    :param conversation_id: uuid of the conversation
    :type conversation_id: str
    :param path: path to the file
    :type path: str
    '''
    timestamp = time.time()
    dump = [
        {
            'uuid': conversation_id, 
            'memory': memory, 
            'timestamp': timestamp, 
            'metadata': ''
        } for memory in memories.split('\n') if memory
    ]

    with open(path, 'w', encoding='utf8') as f:
        json.dump(dump, f)


def start_batch_memory_worker(file: str) -> subprocess.Popen:
    '''
    starts the batch memory update process 
    file is the path to batch memory job json
    '''
    worker = subprocess.Popen(
        [sys.executable, BATCH_MEMORY_WORKER_PATH, file], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True 
    )

    return worker