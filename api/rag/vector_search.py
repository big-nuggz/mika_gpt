import faiss
import numpy as np

from api.rag.embedder import start_embed_worker, get_embed_from_worker


def normalize_embeddings(indices: np.ndarray, embeddings: np.ndarray) -> faiss.Index:
    '''
    returns vector normalized FAISS Index object
    
    :param indices: ids
    :type indices: np.ndarray
    :param embeddings: embedding vectors of data to be searched
    :type embeddings: np.ndarray
    :return: faiss.Index object
    :rtype: Index
    '''
    d = embeddings.shape[1]

    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(d)
    index = faiss.IndexIDMap(index)
    index.add_with_ids(embeddings, indices)

    return index

def search_with_query(query: str, index: faiss.Index, k=5) -> tuple:
    '''
    searches the most similar top k vectors to given search query
    
    :param query: query string
    :type query: str
    :param index: FAISS Index object
    :type index: faiss.Index
    :param k: top k
    :type k: int
    :return: (similarities: list of float, indices: list of int)
    :rtype: tuple
    '''
    worker = start_embed_worker(query)
    query_embedding = np.array(get_embed_from_worker(worker)['embedding'], dtype=np.float32)

    print(f'query: {query}')

    faiss.normalize_L2(query_embedding.reshape(1, -1))

    similarities, indices = index.search(query_embedding.reshape(1, -1), 5)

    return similarities[0].tolist(), indices[0].tolist()