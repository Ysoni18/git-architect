# GitArchitect

An AI-powered Command Line Interface (CLI) tool that performs deep architectural code reviews on local Git commits using localized open-source LLMs. 

## The Engineering Flex
Unlike standard API wrappers, GitArchitect is designed for localized execution constraints:
* **Defensive Parsing:** Automatically filters out binary files, lock-files, and blacklisted directories to prevent blowing up the LLM context window.
* **Smart Concurrency:** Uses `ThreadPoolExecutor` to read large codebases in parallel, while enforcing sequential execution for local LLM inference to prevent VRAM exhaustion and hardware crashes.
* **Real-time Streaming:** Leverages LangChain to stream architectural insights token-by-token back to the terminal.

## Tech Stack
* Python, Click, GitPython
* LangChain, Llama 3 (via Ollama)

## Quick Start
```bash
# Install the package globally
pip install -e .

# Run an analysis against your previous commit
git-architect --target-rev=HEAD~1