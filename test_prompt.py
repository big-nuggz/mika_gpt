import os
import subprocess
import json

from flask import Flask, render_template, request, jsonify, send_file

from openai import OpenAI

from api.file import *
from api.constants import *
from api.conversation import *
from api.data import *
from api.image import *
from api.tokens import get_token_count_from_chat

from api.rag.db_manager import DBManager
from api.rag.vector_search import normalize_embeddings, search_with_query, search_with_queries
from api.rag.interface import save_batch_memory

from static_prompts.compression_prompt import compression_prompt
from static_prompts.default_core_memory import default_core_memory
from static_prompts.memory_extractor_prompt import memory_extractor_prompt
from static_prompts.system_prompt import system_prompt
from static_prompts.title_prompt import title_prompt
from static_prompts.core_memory_update_prompt import core_memory_update_prompt
from static_prompts.recall_prompt import recall_prompt


core_memory = default_core_memory


# init DB
memory_database = DBManager(MEMORY_DB_PATH)

if SUPPLIER == 'OPENAI':
    client = OpenAI(
        api_key = load_api_key(API_KEY_PATH_OPENAI)
    )
elif SUPPLIER == 'GOOGLE':
    client = OpenAI(
        api_key = load_api_key(API_KEY_PATH_GOOGLE), 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )


data = {
    'uuid': '285f0d7c-22fc-4dd6-ac63-39dea2a80f67',
}

file_name = data['uuid'] + '.json'

conversation_data = load_conversation_data(os.path.join(CONVERSATION_HISTORY_PATH, file_name))


# if convo contains image, use model with vision, otherwise use most intelligent text-only model
response_model = MODEL_VISION
if has_image(conversation_data):
    # response_model = MODEL_VISION
    print('this conversation contains image(s)')
else:
    response_model = MODEL_NON_VISION

# model override
# response_model = MODEL_SUMMARIZER

# reply

# completion = client.chat.completions.create(
#     model=response_model, 
#     messages=[system_prompt] + [core_memory] + conversation_data['current_conversation'] + [{'role': 'user', 'content': "Can you make some edits to your core memory? I'm testing something. Let's change your name to Alice! And maybe add some random stuff in there, anything you like."}], 
# )

# completion = client.chat.completions.create(
#     model=MODEL_SUMMARIZER, 
#     messages=[core_memory_update_prompt] + [core_memory] + [{'role': 'system', 'content': "Change my name to Alice. Add a small note that I enjoy cozy winter evenings, handwritten journals, and noticing tiny, poetic details in everyday life."}], 
# )

# completion = client.chat.completions.create(
#     model=response_model, 
#     messages=[memory_extractor_prompt] + conversation_data['current_conversation'], 
# )

# reply = completion.choices[0].message.content

# print_statistics(completion.usage)

# print(reply)

# # save_batch_memory(reply, conversation_data['uuid'], BATCH_MEMORY_JOB_PATH)
# save_batch_memory(reply, 'test', BATCH_MEMORY_JOB_PATH)

# completion = client.chat.completions.create(
#     model=MODEL_SMALL_WORKER, 
#     messages=[recall_prompt] + conversation_data['core_memory'] + conversation_data['current_conversation'][-3:] + [{
#         'role': 'user', 
#         'content': "What was the secret code, by the way?"
#     }], 
# )

# reply = completion.choices[0].message.content

# print_statistics(completion.usage)

# print(f'[{reply}]')

# search_queries = json.loads(reply)

memory_prompt = []

# completion = client.chat.completions.create(
#     model=MODEL_SMALL_WORKER, 
#     messages=[recall_prompt] + conversation_data['core_memory'] + conversation_data['current_conversation'] + [{
#         'role': 'user', 
#         'content': "Thanks thanks. I checked the console and found that no memories were being recalled. I've fixed that issue now. Now for the uh, 3rd or 4th time the charm, can you remember the secret code word I've mentioned before?"
#     }], 
# )

# queries = completion.choices[0].message.content
queries = '''
[
"Secret code word exists for memory testing",
"Recall pipeline surfaces archival memories into the generation context during tests",
"Tests involve injecting retrieved memories into prompts to verify recall functionality"
]
'''
print(f'recall queries: {queries}')
queries = json.loads(queries)
if queries:
    embeddings = memory_database.get_embeddings(conversation_data['uuid'])

    if embeddings is None:
        print('no memories found')
    else:
        index = normalize_embeddings(*embeddings)
        recall_results = search_with_queries(queries, index, RECALL_MAX)

        memory_prompt = [
            {
                'role': 'assistant', 
                'content': "I recalled these memories from archival memory database to help me with response generation. This message is visible to myself only.\n\n"
            }
        ]

        for query, result in zip(queries, recall_results):
            memory_prompt[0]['content'] += f'QUERY: {query}\nRESULT: \n'

            similarities, indices = result
            for similarity, index in zip(similarities, indices):
                if index == -1:
                    continue

                memory = memory_database.retrieve_memory(index)
                memory_prompt[0]['content'] += f'{memory['text']}\n'

print(memory_prompt[0]['content'])
