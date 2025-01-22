import os
import typer
import torch
import librosa
from dotenv import load_dotenv
from rich import print
from ollama import chat, ChatResponse
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC

# load_dotenv()
# api_key = os.getenv('api_key')
# print(api_key)