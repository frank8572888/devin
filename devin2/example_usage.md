# Devin2 Usage Examples

## Basic Usage with API Key

Once you have an API key set up, you can use the main.py script:

```bash
# Set your API key
export OPENAI_API_KEY="your-api-key-here"

# Run a simple task
python main.py "Create a Python script that calculates the Fibonacci sequence"

# Run with custom parameters
python main.py "Analyze a CSV file and create a summary report" \
  --model gpt-3.5-turbo \
  --max-iterations 50 \
  --workspace /tmp/my_project

# Run a file operation task
python main.py "Create a web scraper that extracts headlines from a news website"
```

## Demo Mode (No API Key Required)

For testing and demonstration purposes, use the demo script:

```bash
# Interactive demo selection
python demo.py

# Run specific demo
python demo.py "Calculate factorial and squares using Python"
python demo.py "Create and process CSV data"
python demo.py "Create a file with hello world"

# Custom demo task
python demo.py "Your custom task description here"
```

## Testing

Run the test suites to verify everything works:

```bash
# Basic component tests
python test_basic.py

# Full system test with mock agent
python test_mock_agent.py
```

## Example Tasks

Here are some example tasks that work well with Devin2:

### File Operations
- "Create a directory structure for a Python project with main.py, requirements.txt, and README.md"
- "Read all .txt files in the current directory and count the total number of words"
- "Create a backup script that compresses all Python files into a zip archive"

### Data Processing
- "Generate sample data and save it as CSV, then create a summary statistics report"
- "Read a JSON file and convert it to a formatted table"
- "Create a script that monitors disk usage and logs it to a file"

### Programming Tasks
- "Write a Python class for a simple calculator with basic operations"
- "Create a script that downloads a file from a URL and validates its checksum"
- "Implement a simple web server that serves static files"

### System Administration
- "Check system resources (CPU, memory, disk) and create a status report"
- "Create a log rotation script for application logs"
- "Set up a simple monitoring script that checks if a service is running"

## Configuration Options

You can customize Devin2 behavior through environment variables:

```bash
export DEVIN2_MODEL="gpt-4"                    # LLM model to use
export DEVIN2_MAX_ITERATIONS="100"             # Maximum iterations
export DEVIN2_WORKSPACE="/tmp/devin2_workspace" # Workspace directory
export DEVIN2_LOG_LEVEL="INFO"                 # Logging level
```

## Architecture Overview

Devin2 consists of several key components:

1. **Agent**: The AI agent that plans and executes actions
2. **Controller**: Manages the agent execution loop
3. **Runtime**: Executes bash commands and Python code
4. **Events**: Event-driven communication between components
5. **State**: Tracks agent progress and history

The system follows this flow:
1. User provides a task
2. Agent analyzes the task and plans actions
3. Controller manages the execution loop
4. Runtime executes commands/code
5. Results are fed back to the agent
6. Process repeats until task completion

## Safety Notes

- Devin2 can execute arbitrary commands and code
- Always run in a safe, isolated environment
- Review generated commands before running in production
- Set appropriate iteration and budget limits
- Use workspace directories to contain file operations