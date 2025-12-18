# check content of db
from pprint import pprint

from api.constants import MEMORY_DB_PATH

from api.rag.db_manager import DBManager


db = DBManager(MEMORY_DB_PATH)
cursor = db.db.cursor()

# cursor.execute('SELECT id, conversation_id, role, text, timestamp, metadata FROM archive')
cursor.execute('SELECT id, conversation_id, role, text, timestamp, metadata FROM archive WHERE conversation_id=?', ('285f0d7c-22fc-4dd6-ac63-39dea2a80f67',))
ret = cursor.fetchall()

pprint(ret)
