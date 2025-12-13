import sys
import subprocess
import json

from ..constants import EMBED_WORKER_PATH


def start_embed_worker(text: str) -> subprocess.Popen:
    '''
    starts the embedding process 
    '''
    worker = subprocess.Popen(
        [sys.executable, EMBED_WORKER_PATH, text], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True 
    )

    return worker


def get_embed_from_worker(worker: subprocess.Popen):
    '''
    get the output from embed worker
    '''
    stdout, stderr = worker.communicate()

    if worker.returncode != 0:
        raise RuntimeError(f'Embedding worker error: {stderr}')
    
    return json.loads(stdout)
