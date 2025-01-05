# MikaGPT
ChatGPT-like UI you can run locally. Comes with locally run TTS feature. Requires internet connection and openai API key to run. 
# Installation
## Setting up the environment
### Create a virtual environment (optional, but recommended)
Run this in root directory.
`python -m venv venv`
Activate the venv from cmd.exe.
`venv/Scripts/activate.bat`
### Install requirements
`pip install -r requirements.txt`
## Install pipertts
Get the piper binary from here, and unzip the content in to root directory. Path to piper.exe should be like:
`/piper/piper.exe`
Download and put voice files of your choice in the `/voices`. Make sure to edit `VOICE_PATH` in app.py so that it matches your chosen voice file. 
## Add API key
Create a file called apikey.txt, paste your openai API key inside.
# Run
`python app.py`
It should give you a localhost URL in the console to access from your browser.