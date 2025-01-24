# Cerebrosonic Navigator (cbro)
# Local LLM-enabled Speech-Driven CLI Assistant

## Example Usage

```
python main.py MATRICE QUORTEXT
python main.py llama3.2 cli-output.quortext
```

## Terminology
**Local Matrice**: The Local Matrice serves as the foundation for your Cerebrosonic Navigator, connecting to a local Large Language Model (LLM) like Llama 3.2 to generate responses based on audio input. By specifying the matrice configuration, you can control what model to use for local inference. Local inference capabilities are provided by Ollama.

**Quortext**: The Quortext is a pre-engineered system prompt that acts as a framework for your Cerebrosonic Navigator's response generation. This pre-defined prompt provides a structured starting point for the LLM to generate customized responses, ensuring consistency and coherence in the output. The Quortext is evaluated at Local Matrice inference-time.

## Troubleshoot
- pyaudio requires portaudio on Mac/OSX. brew install portaudio.
- torch confirmed on python3.9. use pyenv to set the global python version before you create the venv.
- must install ffmpeg for realtimestt. brew install ffmpeg.