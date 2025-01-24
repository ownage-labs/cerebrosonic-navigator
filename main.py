import typer
from rich import print
from ollama import chat
from RealtimeSTT import AudioToTextRecorder
from datetime import datetime

app = typer.Typer()

@app.command()
def fuse(matrice: str, quortext: str, distiller: str):

    start_time = datetime.now()
    latency = None
    
    print(f"Fuse initialized --| matrice:{matrice} | quortext:{quortext} | distiller:{distiller}")

    print("Wait until you see the 'recording' prompt then dictate your request...")

    with AudioToTextRecorder() as recorder:
        recorder.start()
        latency = str((datetime.now() - start_time).total_seconds())
        print(f"Time-To Recorder Start: {latency} seconds")
        input("Press Enter to stop recording...")
        recorder.stop()
        text_transcription = recorder.text()
        print(f"Transcription: {text_transcription}")

    latency = str((datetime.now() - start_time).total_seconds())
    print(f"Time to Transription: {latency} seconds")

    # Generate prompt by combining test.quortext file and transcription
    with open(quortext, 'r') as file:
        quortext = file.read()

    print(f"quortext={quortext}")
    print(f"transcription={text_transcription}")
    print(f"distiller={distiller}")

    prompt = quortext + "\n" + text_transcription + "\n" + distiller

    # Call Ollama API
    response = chat(matrice,  messages=[
        {
            'role': 'user',
            'content': prompt,
        },
        ])
    
    print(f"Response: {response}")
    print(f"Response content: {response.message.content}")

    latency = str((datetime.now() - start_time).total_seconds())
    print(f"Time to LLM Response: {latency} seconds")

    # Save response to a file
    # with open("response.txt", "w") as file:
    #     file.write(str(response))
    
if __name__ == "__main__":
    app()