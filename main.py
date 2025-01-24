import os
import typer
import torch
import librosa
import pyaudio
import wave
from dotenv import load_dotenv
from rich import print
from ollama import chat, ChatResponse
from RealtimeSTT import AudioToTextRecorder

# load_dotenv()
# api_key = os.getenv('api_key')
# print(api_key)

# cbro fuse --matrice llama3.2 --quortext cli --distillerator json/raw/xml/yaml

app = typer.Typer()

@app.command()
def fuse(matrice: str, quortext: str, distiller: str):
    
    print(f"Fuse initialized --| matrice:{matrice} | quortext:{quortext} | distiller:{distiller}")

    print("Wait until you see the 'recording' prompt then dictate your request...")

    with AudioToTextRecorder() as recorder:
        recorder.start()
        input("Press Enter to stop recording...")
        recorder.stop()
        text_transcription = recorder.text()
        print(f"Transcription: {text_transcription}")

    # Generate prompt by combining test.quortext file and transcription

    with open(quortext, 'r') as file:
        quortext = file.read()
    prompt = quortext + "\n" + text_transcription
    print(prompt)
    # Call Ollama API
    response = chat(matrice,  messages=[
        {
            'role': 'user',
            'content': prompt,
        },
        ])
    print(f"Response: {response}")
    # Save response to a file
    with open("response.txt", "w") as file:
        file.write(str(response))
    
if __name__ == "__main__":
    app()