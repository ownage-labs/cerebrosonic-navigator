import os
import typer
import torch
import librosa
import pyaudio
import wave
from dotenv import load_dotenv
from rich import print
from ollama import chat, ChatResponse
# import sounddevice as sd
# import soundfile as sf
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
        print("Transcription: ", recorder.text())

    # samplerate = 44100 # hertz
    # duration = 5
    # filename = 'output.wav'

    # mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, blocking=False)
    # sf.write(filename, mydata, samplerate)
    
if __name__ == "__main__":
    app()