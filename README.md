# Cerebrosonic Navigator (cbro)
# Local LLM-enabled Speech-Driven CLI Assistant

## Example Usage

```
python main.py CONFIG
python main.py config.yaml
```

## Troubleshoot
- pyaudio requires portaudio on Mac/OSX. brew install portaudio.
- torch confirmed on python3.9. use pyenv to set the global python version before you create the venv.
- must install ffmpeg for realtimestt. brew install ffmpeg.