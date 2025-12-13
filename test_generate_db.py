# test code for vector/text database testing wow
import json
import time
import numpy as np

from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from api.constants import EMBED_MODEL
from api.rag.db_manager import DBManager


model = SentenceTransformer(EMBED_MODEL)

db_manager = DBManager('./memory/test_db.db')

summaries = []
with open('batch_result.jsonl', 'r', encoding='utf8') as f:
    for line in f:
        summaries.append(json.loads(line))

for summary in tqdm(summaries):
    content = summary['response']['body']['choices'][0]['message']
    role = content['role']
    text = content['content']
    embedding = model.encode(text).tolist()

    db_manager.add_memory(
        'test_convo', 
        role, 
        text, 
        time.time(), 
        '', 
        np.array(embedding, dtype=np.float32)
    )