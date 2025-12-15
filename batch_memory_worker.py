import sys
import json
import numpy as np

from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from api.constants import EMBED_MODEL, MEMORY_DB_PATH
from api.file import load_json

from api.rag.db_manager import DBManager


if len(sys.argv) < 2:
    sys.exit()


memory_database = DBManager(MEMORY_DB_PATH)

model = SentenceTransformer(EMBED_MODEL)

path = sys.argv[1]
batch_job = load_json(path)

for job in tqdm(batch_job):
    embedding = model.encode(job['memory']).tolist()
    memory_database.add_memory(
        job['uuid'], 
        '', # role, unused
        job['memory'], 
        job['timestamp'], 
        job['metadata'], 
        np.array(embedding))

print('batch job completed')