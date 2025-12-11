import sys
import json

from sentence_transformers import SentenceTransformer

from api.constants import EMBED_MODEL


model = SentenceTransformer(EMBED_MODEL)


if len(sys.argv) < 2:
    sys.exit()

text = sys.argv[1]
embedding = model.encode(text).tolist()

print(json.dumps({'embedding': embedding}))