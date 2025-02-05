"""
Cerebrosonic Navigator: A private speech-driven CLI assistant using local LLMs.

This module implements a CLI tool that converts spoken or text input into Unix/Linux
command suggestions using local language models and manual page retrieval for accuracy.

Features:
    - Speech-to-text using RealtimeSTT
    - Local LLM inference using Ollama
    - Function calling and RAG using manual pages
    - YAML-based configuration

Example:
    $ python main.py config.yaml --input "How do I list files?"
    $ python main.py config.yaml --input "How do I check disk space?" --tools
"""

import typer
import yaml
import logging
import subprocess
from typing import Optional
from ollama import chat
from RealtimeSTT import AudioToTextRecorder
import sglang as sgl

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = typer.Typer()

class CerebrosonicNavigator:
    """
    A private CLI assistant using local LLMs and manual page retrieval.

    This class handles the core functionality of processing user input (speech or text)
    and generating appropriate CLI command suggestions with explanations.

    Attributes:
        config_data (dict): Loaded configuration from YAML file
        ollama_model (str): Name of the Ollama model to use
        tasks (dict): Retrieval and summarization prompts
    """

    def __init__(self, config_path: str):
        """
        Initialize the navigator with configuration.

        Args:
            config_path (str): Path to YAML configuration file
        """
        self.config_data = self._load_config(config_path)
        self.ollama_model = self.config_data.get('spec', {}).get('models', {}).get('ollama', 'llama3.2')
        self.tasks = self.config_data.get('spec', {}).get('tasks', {})

        logger.info(f"Initialized with Ollama model: {self.ollama_model}")
        logger.debug(f"Tasks: {self.tasks}")

    def _load_config(self, path: str) -> Optional[str]:
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise typer.Exit(1)

    def transcribe(self) -> str:
        """
        Record and transcribe speech input using RealtimeSTT.

        Returns:
            str: Transcribed text from speech input
        """
        with AudioToTextRecorder() as recorder:
            recorder.start()
            input("Recording started. Press Enter to stop...")
            recorder.stop()
            return recorder.text()

    def get_manpage(self, command: str) -> str:
        """
        Retrieve manual page content for a command.

        Args:
            command (str): Command to get manual page for
            
        Returns:
            str: Manual page content or empty string if not found
        
        Example:
            >>> navigator.get_manpage("ls")
            'LS(1)   User Commands...'
        """
        try:
            command = command.split()[0]
            result = subprocess.run(['man', command], capture_output=True, text=True)
            logger.debug(f"Manpage for {command}:\n{result}")
            return result
        except Exception as e:
            logger.error(f"Error fetching manpage for {command}: {e}")
            return ""

    def navigate_cli(self, user_input: str) -> str:
        """
        Process user input using SGLang for structured command generation.

        Args:
            user_input (str): User's command request

        Returns:
            str: Generated state containing command suggestion and explanation
        
        Example:
            >>> navigator.navigate_cli("How do I list files?")
            {'command_suggestion': 'ls', 'summary': '...explanation...'}
        """
        try:
            # Ollama must be running on port 11434
            backend = sgl.OpenAI(
                model_name=self.ollama_model,
                base_url="http://127.0.0.1:11434/v1",
                api_key="EMPTY"
            )
            sgl.set_default_backend(backend)

            @sgl.function
            def runner(s, input):
                s += sgl.system(self.tasks.get('retrieve'))
                s += sgl.user(input)
                s += sgl.assistant(sgl.gen("command_suggestion", max_tokens=64, temperature=0))
                s += sgl.user(self.tasks.get('summarize'))
                s += sgl.assistant(sgl.gen("summary", max_tokens=256, temperature=0))

            state = runner.run(input=user_input)
            command_suggestion = state["command_suggestion"]
            summary = state["summary"]

            logger.debug(f"Response state: {state}")
            logger.info(f"Command suggestion: {command_suggestion}")
            logger.info(f"Summary: {summary}")

            return state

        except Exception as e:
            logger.error(f"Error processing input: {e}")
            raise typer.Exit(1)    
        
    def navigate_cli_with_tools(self, user_input: str) -> str:
        """
        Process user input using function calling and manual page retrieval.

        Uses Ollama's function calling to retrieve relevant manual pages and
        generates a summary based on the retrieved documentation.

        Args:
            user_input (str): User's command request

        Returns:
            str: Generated summary based on manual page content
        
        Example:
            >>> navigator.navigate_cli_with_tools("How do I check disk space?")
            'Command Overview: The df command shows disk space usage...'
        """
        try:
            logger.info(f"Querying Ollama with model: {self.ollama_model}, user_input: {user_input}")

            response = chat(
                self.ollama_model, 
                messages=[
                {'role': 'system', 'content': self.tasks.get('retrieve')},
                {'role': 'user', 'content': user_input},
                ],
                tools=[self.get_manpage])
            
            logger.info(f"Retrieval Response: {response}")

            available_functions = {
                'get_manpage': self.get_manpage
            }

            function_outputs = []
            for tool in response.message.tool_calls or []:
                function_to_call = available_functions.get(tool.function.name)
                if function_to_call == self.get_manpage:
                    logger.info(f"Calling get_manpage with command: {tool.function.arguments['command']}")
                    output = function_to_call(tool.function.arguments['command'])
                    logger.debug(f"Function output: {output}")
                    function_outputs.append(output)
                else:
                    logger.warning(f"Function not found: {tool.function.name}")

            manpages = f"""{function_outputs}"""
            logger.info(f"Generating manpage summary")

            summary = chat(
                model=self.ollama_model,
                messages=[
                    {'role': 'system', 'content': self.tasks.get('summarize')},
                    {'role': 'user', 'content': user_input},              
                    {'role': 'user', 'content': manpages},
                ]
            )

            logger.info(f"Summary Response: {summary.message.content}")

            return summary.message.content

        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            raise typer.Exit(1)    

@app.command()
def main(
    config_path: str = typer.Argument(..., help="Path to the configuration YAML file"),
    input: str = typer.Option(None, "--input", "-i", help="Optional text input instead of speech"),
    tools: bool = typer.Option(False, "--tools", "-t", help="Use tool-based navigation with manpages")
):
    """
    Cerebrosonic Navigator CLI entry point.

    Processes either speech or text input to suggest appropriate Unix/Linux commands
    with explanations. Can use either direct LLM generation or tool-based retrieval
    augmented generation with manual pages.

    Args:
        config_path: Path to YAML configuration file
        input: Optional text input (uses speech input if not provided)
        tools: Whether to use tool-based navigation with manual pages
    
    Example:
        $ python main.py config.yaml --input "How do I list files?" --tools
    """
    navigator = CerebrosonicNavigator(config_path)
    
    if input:
        logger.info(f"Processing text input: {input}")
        if tools:
            logger.info("Using tool-based navigation with manpages")
            navigator.navigate_cli_with_tools(input)
        else:
            logger.info("Using standard navigation")
            navigator.navigate_cli(input)
    else:
        logger.info("Starting speech recognition...")
        transcribed = navigator.transcribe()
        if tools:
            logger.info("Using tool-based navigation with manpages")
            navigator.navigate_cli_with_tools(transcribed)
        else:
            logger.info("Using standard navigation")
            navigator.navigate_cli(transcribed)

if __name__ == "__main__":
    app()