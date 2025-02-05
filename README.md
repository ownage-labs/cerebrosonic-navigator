# Cerebrosonic Navigator (Example)
Processes either speech or text input to suggest appropriate Unix/Linux commands with explanations. Can use either direct LLM generation or tool-based retrieval augmented generation (agentic RAG) with manual pages.

![Cerebrosonic Navigator](/docs/CerebrosonicNavigator.png)

## Features
- **100% Private & Open Source**: Uses on-device hardware and does not transmit to the cloud.
- **Easy-Swap Models**: Ollama integration to support the latest open source models. 
- **Tool-Use and RAG**: Enhanced command suggestions via real-time tool-based retrieval augmented generation. Examples using Ollama and SGLang.
- **Speech Recognition**: Real-time speech-to-text transcription for spoken navigation.

## On-Device Flow (Tool Use/Function Calling + RAG)
```mermaid
sequenceDiagram
    participant User as User (Speech/Text)
    participant STT as Local Speech-to-Text (RealtimeSTT)
    participant LLM as Local LLM (Ollama/SGL)
    participant Man as Local Manual Pages (Linux)

    User->>STT: Spoken request
    Note over STT: Whisper tiny model
    STT->>LLM: Transcribed text
    User->>LLM: Text request
    Note over LLM: Retrieve
    LLM->>Man: Tool use: get_manpage(command)
    Man->>LLM: Command documentation
    Note over LLM: Summarize
    LLM->>User: Command suggestion + explanation
```

## Example Usage

### Standard Navigation
```bash
$ python main.py config.yaml --input "How do I list all open ports?"
```

<details>
<summary>View output</summary>

```
INFO - Initialized with Ollama model: llama3.2
INFO - Processing text input: How do I list all open ports?
INFO - Using standard navigation
INFO - Processing input with llama3.2

Command suggestion: The netstat command

Explanation: 
**The `netstat` Command**

Command Purpose:
The `netstat` command displays active Internet connections, routing tables, and interface statistics.

Key Features:
* Displays information about active network connections
* Shows listening ports and their corresponding processes
* Provides information on routing tables and interface statistics

Common Use Cases:
* Identifying open ports and the processes using them
* Troubleshooting network connectivity issues
* Monitoring system performance and resource utilization

Related Commands:
The `ss` command is an alternative to `netstat`, offering similar functionality with more detailed information.
```
</details>

### Tool-based Navigation with Manual Pages
```bash
$ python main.py config.yaml --input "How do I list all open ports?" --tools
```

<details>
<summary>View output</summary>

```
INFO - Initialized with Ollama model: llama3.2
INFO - Processing text input: How do I list all open ports?
INFO - Using tool-based navigation with manpages
INFO - Querying Ollama with model: llama3.2
INFO - Calling get_manpage for command: netstat
INFO - Generating manpage summary

Command Overview:
The `netstat` command provides information about active Internet connections, routing tables, 
interface statistics, and more.

Options Available:
* -a, --all: Display all connections
* -i, --interfaces: Display interfaces and their statistics
* -n, --numeric-ports: Show port numbers instead of hostnames
* -p, --protocol: Specify a protocol (e.g., TCP, UDP)
* -r, --routing-table: Display the routing table
* -s, --statistics: Display statistics about interfaces and protocols
```
</details>

## Installation

### 1. System Requirements
```bash
# MacOS (using Homebrew)
brew install portaudio ffmpeg ollama

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3.9 python3.9-dev portaudio19-dev ffmpeg
curl https://ollama.ai/install.sh | sh
```

### 2. Python Environment
```bash
# Create and activate virtual environment
python3.9 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Ollama Model Setup
```bash
# Pull required models
ollama pull llama3.2:latest
ollama pull deepseek-r1:8b

# Verify Ollama is running (default port 11434)
curl http://localhost:11434/api/tags
```

### 4. Configuration
```bash
# Copy example config
cp config.example.yaml config.yaml

# Edit config to select your preferred model
vim config.yaml
```
## License
Apache License 2.0. See [LICENSE](LICENSE) file for details.