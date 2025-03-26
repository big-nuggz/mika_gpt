# paths
API_KEY_PATH_OPENAI = './apikey_openai.txt'
API_KEY_PATH_GOOGLE = './apikey_google.txt'
CONVERSATION_HISTORY_PATH = './chats'
SYSTEM_PROMPT_PATH = './system_prompt.json'
TITLE_PROMPT_PATH = './title_prompt.json'

SUPPLIER = 'GOOGLE' # OPENAI, GOOGLE

# models
if SUPPLIER == 'OPENAI':
    # openai models
    MODEL_VISION = 'gpt-4o'
    MODEL_REASONING = 'o3-mini'
    MODEL_TITLING = 'gpt-4o-mini'

    # image (dall-e)
    DALLE_MODEL = 'dall-e-2'
    IMAGE_RESOLUTION = '256x256'
elif SUPPLIER == 'GOOGLE':
    # google models
    MODEL_VISION = 'gemini-2.0-flash'
    MODEL_REASONING = 'gemini-2.0-flash'
    MODEL_TITLING = 'gemini-2.0-flash-lite'

    # image (imagen)
    DALLE_MODEL = 'imagen-3.0-generate-002'
    IMAGE_RESOLUTION = '256x256'

# tts stuff
PIPER_PATH = './piper/piper.exe'
VOICE_PATH = './voices/en_US_libritts_r_medium_en_US-libritts_r-medium.onnx'
TTS_OUT_PATH = './voice.ogg'



# regex string for image prompt search
IMAGE_PROMPT_SEARCH_STRING = r'\{IMAGE_PROMPT\}(.+)\{\/IMAGE_PROMPT\}'