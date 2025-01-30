# Cerebrosonic Navigator Prototype
## Agentic RAG CLI Assistant

The Cerebrosonic Navigator is a prototype that leverages local Large Language Models (LLMs) to provide a speech-driven command line interface (CLI) assistant. The assistant helps users by interpreting spoken commands, generating appropriate CLI commands, and providing explanations and manpages for those commands.

![Cerebrosonic Navigator](/docs/CerebrosonicNavigator.png)

## Features
- **100% Private**: Utilizes local hardware and models to interpret user commands and generate appropriate CLI commands.
- **Open Source Model Support**: Meta Llama 3.2, DeepSeek-V3, DeepSeek-R1
- **Tool-Use and RAG**: Incorporates tool-use and Retrieval-Augmented Generation (RAG) to enhance the assistant's capabilities.
- **Speech Recognition**: Uses real-time speech-to-text (STT) to transcribe user input for speech-driven local LLM prompting.

## Example Usage

```sh
python main.py CONFIG
python main.py config.yaml
```

## Configuration File

The configuration file should be a YAML file with the following structure:

```yaml
apiVersion: v1
kind: Config
metadata:
  name: cerebrosonic-navigator-config
  description: speech-driven command line expert
  author: ownage-labs
  date: 01/23/2025
spec:
  models:
    ollama: llama3.2
    realtimestt: whisper-tiny
  ooda_loop:
    observe: >
      You are a command line (CLI) expert. 
      Your task is to find the command or combinations of commands that best match the user's input.
      You must be 100% sure your response does not include any arguments or parameters for the commands.
    orient: >
      Analyze the observed data.
      Identify patterns and potential solutions.
      Consider best practices and user requirements.
    decide: >
      Select the most appropriate course of action
      based on the analysis and available options.
    act: >
      Execute the chosen solution.
      Provide clear explanations and code examples.
      Verify the results meet requirements.
```

## Troubleshoot
- **pyaudio** requires portaudio on Mac/OSX. Install it using `brew install portaudio`.
- **torch** confirmed on Python 3.9. Use `pyenv` to set the global Python version before you create the virtual environment.
- Must install **ffmpeg** for real-time STT. Install it using `brew install ffmpeg`.

## License
This project is licensed under the MIT License.