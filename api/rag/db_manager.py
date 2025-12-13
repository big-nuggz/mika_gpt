import sqlite3
import numpy as np


class DBManager():
    '''
    all the DB stuff wrapped in for ez usage
    '''
    def __init__(self, path: str):
        '''
        will create and initialize if DB doesn't exist
        '''
        self.path = path

        self.db = sqlite3.connect(self.path)
        self._init_table()
    
    def _init_table(self):
        '''
        make sure necessary table exists
        '''
        cursor = self.db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            conversation_id TEXT, 
            role TEXT, 
            text TEXT, 
            timestamp REAL,
            metadata TEXT, 
            embedding BLOB
        )
        ''')
        self.db.commit()

    def add_memory(
            self,
            conversation_id: str,  
            role: str, 
            text: str, 
            timestamp: float, 
            metadata: str, 
            embedding: np.ndarray):
        '''
        insert the given data in db
        all entries are necessary

        embedding: float embedding vector of text
        '''
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO archive (conversation_id, role, text, timestamp, metadata, embedding) VALUES (?, ?, ?, ?, ?, ?)', 
            (
                conversation_id, 
                role, 
                text, 
                timestamp, 
                metadata, 
                embedding.astype(np.float32).tobytes()))
        self.db.commit()

    def retrieve_memory(self, memory_id: int) -> dict:
        '''
        specify ID of entry, which is unique globally across all convos
        '''
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT id, role, text, timestamp, metadata FROM archive WHERE id=?', 
            (memory_id,))
        ret = cursor.fetchone()

        if not ret:
            return None
        
        return {
            'role': ret[1], 
            'text': ret[2], 
            'timestamp': ret[3], 
            'metadata': ret[4], 
        }
    
    def get_embeddings(self, conversation_id) -> tuple:
        '''
        returns array of ids and embeddings for every archival memory of specific convo
        pass this onto the vector searcher yay
        '''
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT id, conversation_id, embedding FROM archive WHERE conversation_id=?', 
            (conversation_id,))

        ids = []
        embeddings = []

        for raw_id, _, embedding_blob in cursor.fetchall():
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            ids.append(raw_id)
            embeddings.append(embedding)

        embeddings = np.vstack(embeddings)
        ids = np.array(ids)

        return ids, embeddings