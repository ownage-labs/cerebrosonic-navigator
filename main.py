import typer
import yaml
import logging
import subprocess
from ollama import chat
from RealtimeSTT import AudioToTextRecorder
from rich import print
from datetime import datetime
from typing import Optional, Callable
from functools import wraps
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = typer.Typer()

def measure_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        logger.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            elapsed = (datetime.now() - start).total_seconds()
            logger.info(f"Completed {func.__name__} in {elapsed:.3f} seconds")
            return result
        except Exception as e:
            elapsed = (datetime.now() - start).total_seconds()
            logger.error(f"Failed {func.__name__} after {elapsed:.3f} seconds: {str(e)}")
            raise
    return wrapper

def load_config(path: str) -> Optional[dict]:
    """Load and parse config file."""
    try:
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    except (yaml.YAMLError, FileNotFoundError) as e:
        logger.error(f"Error loading config: {e}")
        raise typer.Exit(1)

def get_transcription() -> str:
    """Record and transcribe audio input. User must press Enter to stop recording."""
    with AudioToTextRecorder() as recorder:
        recorder.start()
        input("Recording started. Press Enter to stop...")
        recorder.stop()
        transcription = recorder.text()
        logger.info(f"Transcription: {transcription}")
        return transcription

def query_llm(model: str, system_prompt: str, user_input: str) -> str:
    """Query the LLM with system prompt and user input."""
    try:
        logger.info(f"Querying LLM with matrice: {model}")
        logger.debug(f"System prompt: {system_prompt[:100]}...")
        logger.debug(f"User input: {user_input}")
        
        response = chat(model, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input},
        ])
        
        logger.info("LLM response received successfully")
        logger.debug(f"Raw response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error querying LLM: {e}")
        raise typer.Exit(1)

def get_manpage(command: str) -> str:
    """Get the manpage for a given command."""
    try:
        result = subprocess.run(['man', command], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        logger.error(f"Error fetching manpage for {command}: {e}")
        return ""

@app.command()
@measure_time
def fuse(
    config: str = typer.Argument(..., help="Path to the configuration YAML file")
):
    """
    Record audio input and process it through a local LLM using the specified quortext.
    """
    logger.info(f"Initializing with config: {config}")    
    config_data = load_config(config)
    logger.info(f"Config data: {config_data}")
    config_model = config_data.get('local_model', '')
    config_quortext = config_data.get('quortext', '')
    config_distiller = config_data.get('distiller', '')

    transcription = get_transcription()

    response = query_llm(config_model, config_quortext, transcription)
    
    print(f"\nResponse: {response}")
    command = response.message.content.strip()
    print(f"\nCommand: {command}")
    manpage = get_manpage(command)
    
    if manpage:
        logger.info(f"Sending manpage for command: {command}")
        response = query_llm(config_model, config_quortext, manpage)
        print(f"\nManpage Response: {response}")

if __name__ == "__main__":
    app()