import tiktoken


# paths
API_KEY_PATH_OPENAI = './apikey_openai.txt'
API_KEY_PATH_GOOGLE = './apikey_google.txt'
CONVERSATION_HISTORY_PATH = './chats'
SYSTEM_PROMPT_PATH = './static_prompts/system_prompt.json'
TITLE_PROMPT_PATH = './static_prompts/title_prompt.json'
COMPRESSION_PROMPT_PATH = './static_prompts/compression_prompt.json'
SUMMARIZER_PROMPT_PATH = './static_prompts/summarizer_prompt.json'

SUPPLIER = 'OPENAI' # OPENAI, GOOGLE

TOKEN_COMPRESSION_LIMIT = 15000 # if token count in chat exceeds this, compress the chat

# models
if SUPPLIER == 'OPENAI':
    # tokenizer
    TOKEN_ENCODER = tiktoken.encoding_for_model('gpt-4o')

    # openai models
    MODEL_VISION = 'gpt-5-chat-latest'
    MODEL_NON_VISION = 'gpt-5-chat-latest'
    MODEL_TITLING = 'gpt-5-nano'
    MODEL_SUMMARIZER = 'gpt-5-nano'

    # image (dall-e)
    DALLE_MODEL = 'dall-e-2'
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

    # image (imagen)
    DALLE_MODEL = 'imagen-3.0-generate-002'
    IMAGE_RESOLUTION = '256x256'

# tts stuff
PIPER_PATH = './piper/piper.exe'
VOICE_PATH = './voices/en_US_libritts_r_medium_en_US-libritts_r-medium.onnx'
TTS_OUT_PATH = './voice.ogg'



# regex string for image prompt search
IMAGE_PROMPT_SEARCH_STRING = r'\{IMAGE_PROMPT\}(.+)\{\/IMAGE_PROMPT\}'