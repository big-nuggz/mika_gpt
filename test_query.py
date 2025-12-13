# test code for vector/text database testing wow wow this one you can test query search
from api.rag.db_manager import DBManager
from api.rag.vector_search import normalize_embeddings, search_with_query


query = 'farming, gardening'

db_manager = DBManager('./memory/test_db.db')

ids, vectors = db_manager.get_embeddings('test_convo')

index = normalize_embeddings(ids, vectors)
similarities, indices = search_with_query(query, index, 5)

for similarity, index in zip(similarities, indices):
    entry = db_manager.retrieve_memory(index)

    print(f'matched id: {index}')
    print(f'distance: {similarity}')

    print(entry)

    print(f'\n{"-"*40}\n')