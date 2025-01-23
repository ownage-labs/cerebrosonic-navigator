# Cerebrosonic Navigator (cbro)

## Example Usage

```
cbro fuse --matrice llama3.2 --cortex cli --granulator json/raw/xml/yaml
cbro configure matrice llama3.2 (ollama model)
cbro configure cortex cli-commands (system prompt + few-shot examples)
cbro configure granulator json/raw/xml/yaml (output format)
```

## Terminology
**Matrice**: The Matrice serves as the foundation for your Cerebrosonic 
Navigator, connecting to a Large Language Model (LLM) like Llama 3.2 
to generate responses based on user input, via Ollama. By specifying the matrice configuration, you can control what model to use for local inference. 

**Cortex**: The Cortex is a pre-built system prompt that acts as a 
framework for your Cerebrosonic Navigator's response generation. This 
pre-defined prompt provides a structured starting point for the LLM 
to generate customized responses, ensuring consistency and coherence 
in the output. The Cortex is evaluated at Matrice inference-time.

**Granulator**: The Granulator takes the generated response from the 
LLM and refines it into a formatted, user-friendly output. By 
specifying the granulator configuration, you can customize the 
presentation of the final response, including formatting options, 
tone, and style, to create a seamless user experience.

## Troubleshoot
- pyaudio requires portaudio on Mac/OSX. brew install portaudio.
- torch confirmed on python3.9. use pyenv to set the global python version before you create the venv.