# paths
API_KEY_PATH = './apikey.txt'
CONVERSATION_HISTORY_PATH = './chats'
SYSTEM_PROMPT_PATH = './system_prompt.json'
TITLE_PROMPT_PATH = './title_prompt.json'

# models
MODEL_VISION = 'gpt-4o'
MODEL_REASONING = 'o3-mini'
MODEL_TITLING = 'gpt-4o-mini'

# tts stuff
PIPER_PATH = './piper/piper.exe'
VOICE_PATH = './voices/en_US_libritts_r_medium_en_US-libritts_r-medium.onnx'
TTS_OUT_PATH = './voice.ogg'

# image (dall-e)
DALLE_MODEL = 'dall-e-2'
IMAGE_RESOLUTION = '256x256'

# regex string for image prompt search
IMAGE_PROMPT_SEARCH_STRING = r'\{IMAGE_PROMPT\}(.+)\{\/IMAGE_PROMPT\}'