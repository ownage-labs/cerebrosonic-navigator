# Cerebrosonic Navigator (cbro)
# Local Audio-Enabled AI CLI Assistant

## Example Usage

```
cbro fuse --matrice llama3.2 --quortext cli --distillerator json/raw/xml/yaml
matrice llama3.2 (ollama model)
quortext file://cli-commands.quortext (system prompt + few-shot examples)
distiller json/raw/xml/yaml (output format)
```

## Terminology
**Local Matrice**: The Local Matrice serves as the foundation for your Cerebrosonic Navigator, connecting to a local Large Language Model (LLM) like Llama 3.2 to generate responses based on audio input. By specifying the matrice configuration, you can control what model to use for local inference. Local inference capabilities are provided by Ollama.

**Quortext**: The Quortext is a pre-engineered system prompt that acts as a framework for your Cerebrosonic Navigator's response generation. This pre-defined prompt provides a structured starting point for the LLM to generate customized responses, ensuring consistency and coherence in the output. The Quortext is evaluated at Local Matrice inference-time.

**Distiller**: The Distiller takes the generated response from the LLM and refines it into a formatted, user or machine friendly output. By specifying the distiller configuration, you can customize the presentation of the final response, including formatting options, tone, and style, to create a seamless user experience.

## Troubleshoot
- pyaudio requires portaudio on Mac/OSX. brew install portaudio.
- torch confirmed on python3.9. use pyenv to set the global python version before you create the venv.
- must install ffmpeg for realtimestt. brew install ffmpeg.