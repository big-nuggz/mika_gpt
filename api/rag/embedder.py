import sys
import subprocess
import json

from ..constants import EMBED_WORKER_PATH


def start_embed_worker(texts: list) -> subprocess.Popen:
    '''
    starts the embedding process

    input: list of strings 
    '''
    worker = subprocess.Popen(
        [sys.executable, EMBED_WORKER_PATH], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True 
    )

    worker.stdin.write(json.dumps(texts))
    worker.stdin.close()

    return worker


def get_embed_from_worker(worker: subprocess.Popen):
    '''
    get the output from embed worker
    '''
    stdout, stderr = worker.communicate()

    if worker.returncode != 0:
        raise RuntimeError(f'Embedding worker error: {stderr}')
    
    return json.loads(stdout)
