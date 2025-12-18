import sys
import json

from sentence_transformers import SentenceTransformer

from api.constants import EMBED_MODEL


data = input()
data = json.loads(data)

model = SentenceTransformer(EMBED_MODEL)

embeddings = []
for text in data:
    embedding = model.encode(text).tolist()
    embeddings.append(embedding)

print(json.dumps(embeddings))