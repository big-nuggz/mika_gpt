import tiktoken


# paths
API_KEY_PATH_OPENAI = './apikey_openai.txt'
API_KEY_PATH_GOOGLE = './apikey_google.txt'
CONVERSATION_HISTORY_PATH = './chats'

SUPPLIER = 'OPENAI' # OPENAI, GOOGLE

TOKEN_COMPRESSION_LIMIT = 10000 # if token count in chat exceeds this, compress the chat

# models
if SUPPLIER == 'OPENAI':
    # tokenizer
    TOKEN_ENCODER = tiktoken.get_encoding('o200k_base')

    # openai models
    MODEL_VISION = 'gpt-6-luna' # honestly the smallest models now are even smarter than the old large models like gpt-4o, so might as well save on the token costs
    MODEL_NON_VISION = 'gpt-6-luna'
    MODEL_TITLING = 'gpt-6-luna' # tiniest model for titling
    MODEL_SUMMARIZER = 'gpt-6-luna'
    MODEL_SMALL_WORKER = 'gpt-6-luna' # used for memory update and such, where small cheap model is enough

    # image (dall-e)
    DALLE_MODEL = 'gpt-image-2'
    IMAGE_RESOLUTION = '256x256'
elif SUPPLIER == 'GOOGLE':
    # tokenizer
    # TODO fill this
    # TOKEN_ENCODER = 

    # google models
    MODEL_VISION = 'gemini-2.0-flash'
    MODEL_NON_VISION = 'gemini-2.0-flash'
    MODEL_TITLING = 'gemini-2.0-flash-lite'
    MODEL_SUMMARIZER = 'gemini-2.0-flash-lite'
    MODEL_SMALL_WORKER = 'gemini-2.0-flash-lite'

    # image (imagen)
    DALLE_MODEL = 'imagen-3.0-generate-002'
    IMAGE_RESOLUTION = '256x256'

# text embedding model, from HF
EMBED_MODEL = 'intfloat/multilingual-e5-small' # this one's reasonably small and fast to run locally
EMBED_WORKER_PATH = 'embed_worker.py'

# tts stuff
PIPER_PATH = './piper/piper.exe'
VOICE_PATH = './voices/en_US_libritts_r_medium_en_US-libritts_r-medium.onnx'
TTS_OUT_PATH = './voice.ogg'

# long-term memory storage path
MEMORY_DB_PATH = './memory/archive.db'

# maximum number of memories to be recalled per search query
RECALL_MAX = 5

# batch memory update worker path
BATCH_MEMORY_WORKER_PATH = 'batch_memory_worker.py'

# temporary batch memory job json file path
BATCH_MEMORY_JOB_PATH = 'batch_memory.json'

# regex string for image prompt search
IMAGE_PROMPT_SEARCH_STRING = r'\{IMAGE_PROMPT\}(.+)\{\/IMAGE_PROMPT\}'

# regex string for core memory update prompt search
CORE_MEMORY_UPDATE_PROMPT_SEARCH_STRING = r'\{CORE\}(.*?)\{\/CORE\}'

# reasoning
REASONING_EFFORT = 'none' # I don't think it's necessary, but you can set it to low if you want to