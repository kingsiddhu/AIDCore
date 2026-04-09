
![Python](https://img.shields.io/badge/Python-3.14.3-blue.svg?style=for-the-badge&labelColor=101418&color=9ccbfb)
![Ollama](https://img.shields.io/badge/LLM-Ollama-black.svg?style=for-the-badge&labelColor=101418&color=b9c8da)
![Status](https://img.shields.io/badge/Status-Experimental-orange.svg?style=for-the-badge&labelColor=101418&color=F3C27C)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg?style=for-the-badge&labelColor=101418&color=9AF47C)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-blue.svg?style=for-the-badge&labelColor=101418&color=9ccbfb)
![Agentic AI](https://img.shields.io/badge/AI-Agentic-blueviolet.svg?style=for-the-badge&labelColor=101418&color=8B82ED)
![Spotify API](https://img.shields.io/badge/Spotify-Integrated-1DB954.svg?style=for-the-badge&labelColor=101418&color=9AF47C)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-purple.svg?style=for-the-badge&labelColor=101418&color=EC7BF4)

<h1 align=center>AIDCore</h1>

![GitHub last commit](https://img.shields.io/github/last-commit/kingsiddhu/AIDCore?style=for-the-badge&labelColor=101418&color=9ccbfb)
[![GitHub Repo stars](https://img.shields.io/github/stars/kingsiddhu/AIDCore?style=for-the-badge&labelColor=101418&color=EAF47B)](https://github.com/kingsiddhu/AIDCore/stargazers)
![GitHub forks](https://img.shields.io/github/forks/kingsiddhu/AIDCore?style=for-the-badge&labelColor=101418&color=F3C27C)
![GitHub repo size](https://img.shields.io/github/repo-size/kingsiddhu/AIDCore?style=for-the-badge&labelColor=101418&color=d3bfe6)
![GitHub watchers](https://img.shields.io/github/watchers/kingsiddhu/AIDCore?style=for-the-badge&labelColor=101418&color=b9c8da)
![GitHub issues](https://img.shields.io/github/issues/kingsiddhu/AIDCore?style=for-the-badge&labelColor=101418&color=9AF47C)

<p align=center>If you like this project, consider giving it a ⭐</p>

AIDCore is a hobby agentic AI system I have been working on to manage and interact with a local computer.

## Overview

AIDCore is currently a backend-only system. I do plan on making a frontend interface once everything is setup properly.

AIDCore can:

- Search, read, write, and modify local files
- Open and view images
- Control and play music via Spotify
- Execute custom command that you define.

## Tech Stack

- **Language:** Python
- **Core Libraries:**

  - `langgraph`
  - `langchain-ollama`
  - `spotipy`

## Features

- Local file system interaction (read, write, navigate)
- Spotify integration for music control
- Agent-based execution loop for task handling
- Extensible architecture for adding tools and capabilities
- Debug mode for testing and development

## Installation


### 1. Install Ollama

Download and install from:
[https://ollama.com](https://ollama.com)

Verify installation:

```bash
ollama --version
```

---

### 2. Download Models


```bash
ollama pull llama3
ollama pull phi3:mini
ollama pull deepseek-coder:6.7b
ollama pull qwen3.5:9b
ollama pull llama3.1:8b
ollama pull deepseek-r1:14b
```

---

### 3. Start the Model Server

Run Ollama (if not already running):

```bash
ollama serve
```

---

### 4. Clone the repository:

```bash
git clone https://github.com/kingsiddhu/AIDCore.git
cd AIDCore
```
---

### 5. Create environment
```bash
python -m venv venv
```

Activate it:

Linux / macOS
```bash
source venv/bin/activate
```
Windows
```powershell
venv\Scripts\activate
```
Install dependencies:

```bash
pip install -r requirements.txt
```


### 6. Environment Variables


AIDCore requires Spotify API credentials with a valid spotify premium subscription to enable music control.\
Set the following environment variables:

* `SP_CLIENT_ID`
* `SP_CLIENT_SECRET`

---

### Linux / macOS (bash / zsh)

Temporary (current session only):

```bash
export SP_CLIENT_ID="your_client_id"
export SP_CLIENT_SECRET="your_client_secret"
```

Permanent (add to shell config):

```bash
echo 'export SP_CLIENT_ID="your_client_id"' >> ~/.bashrc
echo 'export SP_CLIENT_SECRET="your_client_secret"' >> ~/.bashrc
source ~/.bashrc
```

If using zsh:

```bash
echo 'export SP_CLIENT_ID="your_client_id"' >> ~/.zshrc
echo 'export SP_CLIENT_SECRET="your_client_secret"' >> ~/.zshrc
source ~/.zshrc
```

---

### Windows (PowerShell)

Temporary:

```powershell
$env:SP_CLIENT_ID="your_client_id"
$env:SP_CLIENT_SECRET="your_client_secret"
```

Permanent:

```powershell
setx SP_CLIENT_ID "your_client_id"
setx SP_CLIENT_SECRET "your_client_secret"
```

Restart your terminal after running `setx`.

---

### Verify Variables

Check if they are set correctly:

```bash
echo $SP_CLIENT_ID
echo $SP_CLIENT_SECRET
```

On Windows (PowerShell):

```powershell
echo $env:SP_CLIENT_ID
echo $env:SP_CLIENT_SECRET
```

## Usage

Run the main agent:

```bash
python -m runner
#or 
python -m runner -p Your prompt here
```
> [!TIP]
> To run the program in debug mode just add the `--debug` flag\
> Examples:
> ```bash
> python -m runner --debug
> #or 
> python -m runner --debug -p Your prompt here
> ```

## Custom Tools System
> [!NOTE]
> AIDCore supports user-defined tools to extend the capabilities of the agent.
> All tools are defined in `Agent/tools.py`


### Adding Custom Tools
---

To add a new tool, define a function in this file in the section `ADD TOOLS HERE`.

Each tool should:
- Have a clear and descriptive function name
- Accept structured inputs using keyword arguments. All parameters should have default values when possible.
- Return a clean, structured output (string, dict, or JSON-serializable data)
- Be self-contained and avoid side effects unless necessary

Example:

```python
def get_system_uptime():
    """Returns system uptime."""
    return os.popen("uptime -p").read()
```
The system will automatically register it with the AI.

Custom tools can be used for:
- System control
- File operations
- Network tasks
- API integrations
- Automation scripts
- Anything that can be executed programmatically

*I mean technically anything ig*

## Notes

- This is an experimental system and is behaving unpredictably depending on prompts and tools. be careful on what you do with it and any damage to your system is not my responsibility.

## Future Improvements

- Smart Multimodel router
- Frontend interface for easier interaction
- More robust tool handling and safety controls
- Expanded system-level automation capabilities
- Improved memory and planning for the agent
- Hopefully computer vision capabilities.
- Ability to operate real world instruments.

## Authors:

- [Siddharth](https://github.com/kingsiddhu)

## Star History


<a href="https://www.star-history.com/?repos=kingsiddhu%2FAIDCore&type=timeline&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=kingsiddhu/AIDCore&type=timeline&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=kingsiddhu/AIDCore&type=timeline&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=kingsiddhu/AIDCore&type=timeline&legend=top-left" />
 </picture>
</a>