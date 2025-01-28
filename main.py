import typer
import yaml
import logging
import subprocess
from typing import Optional
from ollama import chat
from RealtimeSTT import AudioToTextRecorder
from rich import print

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = typer.Typer()

class CerebrosonicNavigator:
    def __init__(self, config_path: str):
        self.config_data = self.load_config(config_path)
        self.local_model = self.config_data.get('spec', {}).get('models', {}).get('ollama', 'llama3.2')
        self.realtimestt_model = self.config_data.get('spec', {}).get('models', {}).get('realtimestt', 'whisper-tiny')
        self.ooda_loop = self.config_data.get('spec', {}).get('ooda_loop', {})

    def load_config(self, path: str) -> Optional[str]:
        """Load config file."""
        try:
            with open(path, 'r') as file:
                config_data = yaml.safe_load(file)
                return config_data
        except (yaml.YAMLError, FileNotFoundError) as e:
            logger.error(f"Error loading config: {e}")
            raise typer.Exit(1)

    def get_transcription(self) -> str:
        """Record and transcribe audio input. User must press Enter to stop recording."""
        with AudioToTextRecorder() as recorder:
            recorder.start()
            input("Recording started. Press Enter to stop...")
            recorder.stop()
            transcription = recorder.text()
            return transcription

    def query_llm(self, system_prompt: str, user_input: str) -> str:
        """Query the LLM with system prompt and user input."""
        try:
            response = chat(self.local_model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input},
            ])
            return response
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)

    def get_manpage(self, command: str) -> str:
        """
        Get the manpage for a given command.
        
        Args:
            command (str): The command to get the manpage for.

        Returns:
            str: The manpage for the command.
        """
        try:
            result = subprocess.run(['man', command], capture_output=True, text=True)
            print(f"Manpage for {command}:\n{result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching manpage for {command}: {e}")
            return ""

    def observe(self, user_input: str) -> str:
        """Find commands associated with user's input."""
        try:
            print(f"Querying Ollama with model: {self.local_model}, ooda_loop: {self.ooda_loop}, user_input: {user_input}")
            print(f"Observation: {self.ooda_loop.get('observe')}")

            response = chat(
                self.local_model, 
                messages=[
                {'role': 'system', 'content': self.ooda_loop.get('observe')},
                {'role': 'user', 'content': user_input},
                ],
                tools=[self.get_manpage])
            
            print(f"Observe Response: {response}")

            available_functions = {
                'get_manpage': self.get_manpage
            }

            for tool in response.message.tool_calls or []:
                function_to_call = available_functions.get(tool.function.name)
                if function_to_call == self.get_manpage:
                    print(f"Calling get_manpage with command: {tool.function.arguments['command']}")
                    print(f"Function output: {function_to_call(tool.function.arguments['command'])}")
                else:
                    print(f"Function not found: {tool.function.name}")

        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)    
        
        return response

    def orient(self, observables: str) -> str:
        """Read through the manpages to find the best command and arguments."""
        try:
            print(f"Querying Ollama with model: {self.local_model}, role: {self.role}, user_input: {observables}")
            response = chat(
                self.local_model, 
                messages=[
                {'role': 'system', 'content': self.role},
                {'role': 'user', 'content': observables},
                {'role': 'assistant', 'content': 'test'}
                ],
            )
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)    
        return response

    def decide(self, orientables: str) -> str:
        """Decide which command to use."""
        try:
            print(f"Querying Ollama with model: {self.local_model}, role: {self.role}, user_input: {orientables}")
            response = chat(
                self.local_model, 
                messages=[
                {'role': 'system', 'content': self.role},
                {'role': 'user', 'content': orientables},
                ],
            )
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)    
        return response

    def act(self, decidables: str) -> str:
        """Provide response to user based on OOD input."""
        try:
            print(f"Querying Ollama with model: {self.local_model}, role: {self.role}, user_input: {decidables}")
            response = chat(
                self.local_model, 
                messages=[
                {'role': 'system', 'content': self.role},
                {'role': 'user', 'content': decidables},
                ],
            )
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)    
        return response

@app.command()
def fuse(
    config_path: str = typer.Argument(..., help="Path to the configuration YAML file")
):
    """
    Record audio input and process it through a local LLM using tool-use RAG to implement an OODA loop for CLI command generation.
    """
    logger.info(f"Initializing with config: {config_path}")    

    navigator = CerebrosonicNavigator(config_path)
    
    logger.info(f"Config data: {navigator.config_data}")

    navigator.observe(navigator.get_transcription())
   
if __name__ == "__main__":
    app()