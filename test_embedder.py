# test code
from api.embedder import *


if __name__ == '__main__':

    text = """
    hello, this is just some random string of text to be used to create embedding wow so cool yowser
    will it work with multi line text? who knows let's test it yoohooo
    woowowooo
    wawaweewa
    """

    # start the worker
    worker = start_embed_worker(text)

    # do some stuff while worker is running
    import time
    import numpy as np
    for _ in range(100): # waits 10 sec
        print('just doing random stuff to pass the time ' + chr(np.random.randint(ord('A'), ord('z'))), end='\r')
        time.sleep(0.1)
    print()

    # get the stuff and display
    embedding = get_embed_from_worker(worker)

    print(embedding)