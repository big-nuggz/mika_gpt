from pathlib import Path


BASE = Path(__file__).resolve().parent / 'prompt_md' # root of prompts

SYSTEM_PROMPT_PATH = 'system.md'
TITLE_PROMPT_PATH = 'title.md'
COMPRESSION_PROMPT_PATH = 'compression.md'
CORE_MEMORY_UPDATE_PROMPT_PATH = 'core_memory_update.md'
DEFAULT_CORE_MEMORY_PATH = 'default_core_memory.md'
MEMORY_EXTRACTOR_PROMPT_PATH = 'memory_extractor.md'
RECALL_PROMPT_PATH = 'recall.md'


def _load_prompt(path: str, role='system') -> dict:
    '''
    load markdown prompt
    or any text file really lol

    :param path: path to file
    :type path: str
    :param role: role of the prompt
    :type role: str
    :return: loaded prompt
    :rtype: dict
    '''
    with open(path, 'r', encoding='utf8') as f:
       prompt_text = f.read()

    prompt = {
        "role": role, 
        "content": prompt_text
    }

    return prompt
 
# loosely based on MemGPT's prompt, thanks to the lovely people who made it!
# source: https://github.com/letta-ai/letta/blob/main/letta/prompts/system_prompts/memgpt_chat.py (licensed under Apache 2.0 license)
# used Gemini to optimize my hand written prompt (2026-03-20)
# kinda meta isn't it heehe
system_prompt = _load_prompt(BASE / SYSTEM_PROMPT_PATH)

title_prompt = _load_prompt(BASE / TITLE_PROMPT_PATH)
compression_prompt = _load_prompt(BASE / COMPRESSION_PROMPT_PATH)
core_memory_update_prompt = _load_prompt(BASE / CORE_MEMORY_UPDATE_PROMPT_PATH)
default_core_memory = _load_prompt(BASE / DEFAULT_CORE_MEMORY_PATH)
memory_extractor_prompt = _load_prompt(BASE / MEMORY_EXTRACTOR_PROMPT_PATH)
recall_prompt = _load_prompt(BASE / RECALL_PROMPT_PATH)
