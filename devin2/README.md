# Devin2 - Simplified AI Agent

A streamlined implementation of an AI agent that can execute bash commands and Python code to complete tasks, inspired by the original Devin project.

## Features

- 🤖 **Simple Agent**: Execute bash commands and Python code
- 🔄 **Event-driven Architecture**: Clean separation between components
- 📊 **State Management**: Track agent progress and metrics
- 💰 **Cost Tracking**: Monitor LLM usage and costs
- 🛠️ **Runtime Environment**: Safe execution of commands and code

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # or
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Run a task:**
   ```bash
   python main.py "Create a Python script that calculates the factorial of 10"
   ```

## Usage Examples

### Basic Task
```bash
python main.py "List all files in the current directory and count them"
```

### File Operations
```bash
python main.py "Create a CSV file with sample data and then read it with pandas"
```

### Data Processing
```bash
python main.py "Download a JSON file from an API and extract specific fields"
```

### Custom Configuration
```bash
python main.py "Write a simple web scraper" \
  --model gpt-3.5-turbo \
  --max-iterations 50 \
  --workspace /tmp/my_workspace
```

## Command Line Options

- `task`: The task for the agent to complete (required)
- `--model`: LLM model to use (default: gpt-4)
- `--max-iterations`: Maximum number of iterations (default: 100)
- `--workspace`: Workspace directory (default: /tmp/devin2_workspace)
- `--api-key`: API key for LLM (can also use environment variables)
- `--base-url`: Custom base URL for LLM API

## Architecture

```
devin2/
├── main.py              # Main entry point
├── core/                # Core state and configuration
│   ├── state.py         # Agent state management
│   └── config.py        # Configuration handling
├── events/              # Event system
│   ├── event.py         # Base event classes
│   ├── action.py        # Action events
│   ├── observation.py   # Observation events
│   └── stream.py        # Event stream management
├── agent/               # Agent implementation
│   ├── base_agent.py    # Base agent interface
│   ├── simple_agent.py  # Simple agent implementation
│   └── llm.py           # LLM interface
├── controller/          # Agent controller
│   └── agent_controller.py
└── runtime/             # Runtime environment
    └── runtime.py       # Command and code execution
```

## How It Works

1. **Task Input**: You provide a task description
2. **Agent Planning**: The LLM agent analyzes the task and plans actions
3. **Action Execution**: The runtime executes bash commands or Python code
4. **Observation**: Results are fed back to the agent
5. **Iteration**: The process repeats until the task is complete

## Supported Actions

- `<execute_bash>command</execute_bash>`: Execute shell commands
- `<execute_ipython>code</execute_ipython>`: Execute Python code
- `<finish>result</finish>`: Complete the task with results

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `DEVIN2_MODEL`: Default model to use
- `DEVIN2_MAX_ITERATIONS`: Default max iterations
- `DEVIN2_WORKSPACE`: Default workspace directory

## Safety Notes

- The agent can execute arbitrary commands and code
- Use in a safe, isolated environment
- Review generated commands before running in production
- Set appropriate iteration and budget limits

## License

MIT License - see original Devin project for inspiration.