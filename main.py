import typer
import yaml
import logging
import subprocess
import sglang as sgl
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
        self.ollama_model = self.config_data.get('spec', {}).get('models', {}).get('ollama', 'llama3.2')
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

    def transcribe(self) -> str:
        """Record and transcribe audio input. User must press Enter to stop recording."""
        with AudioToTextRecorder() as recorder:
            recorder.start()
            input("Recording started. Press Enter to stop...")
            recorder.stop()
            transcription = recorder.text()
            return transcription

    def query_ollama(self, system_prompt: str, user_input: str) -> str:
        """Query the LLM with system prompt and user input."""
        try:
            response = chat(self.ollama_model, messages=[
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
            command = command.split()[0]
            result = subprocess.run(['man', command], capture_output=True, text=True)
            print(f"Manpage for {command}:\n{result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching manpage for {command}: {e}")
            return ""

    def navigate_cli_with_ollama(self, user_input: str) -> str:
        """Find commands associated with user's input."""
        try:
            print(f"Querying Ollama with model: {self.ollama_model}, user_input: {user_input}")
            print(f"Observe YAML Content: {self.ooda_loop.get('observe')}")

            response = chat(
                self.ollama_model, 
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

    def navigate_bash_cli_with_sglang(self, user_input: str) -> str:
        """Find commands associated with user's input."""
        
        try:
            print(f"Querying Ollama with model: {self.ollama_model}, user_input: {user_input}")

            backend = sgl.OpenAI(
                model_name=self.ollama_model,
                base_url="http://127.0.0.1:11434/v1",
                api_key="EMPTY"
            )
            sgl.set_default_backend(backend)

            @sgl.function
            def ooda_loop(s, input):
                s += sgl.system("You are a Bash command line (CLI) expert. Your task is to find the command or combinations of commands that best match the user's input. You must be 100% sure your response does not include any arguments or parameters.")
                s += sgl.user(input)
                s += sgl.assistant(sgl.gen("manpages", max_tokens=256))

            state = ooda_loop.run(input=user_input)

            for m in state.messages():
                print(m["role"], ":", m["content"])

            print(state["manpages"])

        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)    
        
        return "test"

@app.command()
def fuse(
    config_path: str = typer.Argument(..., help="Path to the configuration YAML file")
):
    """
    Record audio input and process it through a locally hosted LLM including tool-use and RAG to improve accuracy.
    """
    logger.info(f"Initializing with config: {config_path}")    

    navigator = CerebrosonicNavigator(config_path)
    
    logger.info(f"Config data: {navigator.config_data}")

    navigator.navigate_bash_cli_with_sglang(navigator.transcribe())
 
if __name__ == "__main__":
    app()