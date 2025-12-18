# test code for vector/text database testing wow wow this one you can test query search
from api.rag.db_manager import DBManager
from api.rag.vector_search import normalize_embeddings, search_with_queries, search_with_query

from api.constants import MEMORY_DB_PATH


queries = ["User's view on pineapple pizza", "User has mentioned a secret code"]

db_manager = DBManager(MEMORY_DB_PATH)

ret = db_manager.get_embeddings('285f0d7c-22fc-4dd6-ac63-39dea2a80f67')

if ret is None:
    raise TypeError('no embeddings found')

ids, vectors = ret

index = normalize_embeddings(ids, vectors)
results = search_with_queries(queries, index, 50)

for query, result in zip(queries, results):
    print(f'query: {query}')

    similarities, indices = result
    for similarity, index in zip(similarities, indices):
        entry = db_manager.retrieve_memory(index)

        print(f'matched id: {index}')
        print(f'distance: {similarity}')

        print(entry)

        print(f'\n{"-"*40}\n')