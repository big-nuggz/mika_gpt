# MikaGPT
![screenshot](screenshot.png)
ChatGPT-like UI you can run locally. Uses [Flask](https://flask.palletsprojects.com/en/stable/) as backend. Requires internet connection and LLM API key to run (or, technically, locally hosted LLM too, but requires additional configuration which will not be documented here).

## Features
- Runs on Flask backend via Python, with web interface frontend for easy use. 
- Manage multiple chats.
- Cute pink UI.
- Good personality (customizable).
- Vision and image gen support (requires compatible models).
- Locally run TTS synthesis (requires Piper installation).
- Chat compression system for unlimited chat length.

### The chat compression
Basically, when the chat token length exceeds the user specified limit, chat will automatically be compressed while retaining as much context as possible. Compression happens silently to user, and it offers seamless continuation of the chat, giving an illusion of unlimited chat while keeping the token count low.

## Installation
### Create a virtual environment (optional, but recommended)
Run this in root directory.
`python -m venv ./venv`
Activate the venv from cmd.exe.
`venv/Scripts/activate.bat`

### Install requirements
`pip install -r requirements.txt`

### Install Piper TTS
Get the Piper binary from [here](https://github.com/rhasspy/piper), and unzip the content in to root directory. Path to piper.exe should be like:
`./piper/piper.exe`
Download and put voice files of your choice in the `./voices`. Make sure to edit `VOICE_PATH` in `./api/constants.py` so that it matches your chosen voice file. 

### Add API key
Create a file called `./apikey_openai.txt` or `./apikey_google.txt`, paste your openai/google API key inside.

### Configure model
You can either use OpenAI models or Google models. Google models as of now can be used for free (but they will collect your data). OpenAI models requires paid API access.

`./api/constants.py` for model configurations. See the source for further information.

### Edit system prompts
Inside `./static_prompts`, you can edit system prompts to change the behavior and personality of the AI. I suggest not touching the `title_prompt.json` and `compression_prompt.json` as those 2 are used for tasks unrelated to chat itself.

## Run
`python app.py`
It should give you a localhost URL in the console to access from your browser.

**WARNING** do NOT try host this on remote server, it is not secure. This app is intended for local use only.