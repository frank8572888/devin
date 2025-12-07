#!/usr/bin/env python3
"""
Demo script showing Devin2 capabilities without requiring API keys.
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.state import State, AgentState
from events.stream import EventStream, EventSource
from events.action import MessageAction, CmdRunAction, IPythonRunCellAction, AgentFinishAction
from controller.agent_controller import AgentController
from agent.base_agent import BaseAgent
from runtime.runtime import Runtime


class DemoAgent(BaseAgent):
    """A demo agent that showcases various capabilities."""
    
    def __init__(self, task: str, name: str = "DemoAgent"):
        super().__init__(name)
        self.task = task
        self.step_count = 0
        
        # Define different demo scripts based on task
        if "file" in task.lower() and "create" in task.lower():
            self.script = self._file_creation_script()
        elif "python" in task.lower() or "calculate" in task.lower():
            self.script = self._python_calculation_script()
        elif "data" in task.lower() or "csv" in task.lower():
            self.script = self._data_processing_script()
        else:
            self.script = self._general_demo_script()
    
    def _file_creation_script(self):
        return [
            CmdRunAction("pwd", "Checking current directory"),
            CmdRunAction("echo 'Hello, World!' > hello.txt", "Creating a simple text file"),
            CmdRunAction("cat hello.txt", "Reading the file content"),
            CmdRunAction("ls -la *.txt", "Listing text files"),
            AgentFinishAction({"result": "Successfully created and read a text file"})
        ]
    
    def _python_calculation_script(self):
        return [
            IPythonRunCellAction("import math", "Importing math module"),
            IPythonRunCellAction("numbers = [1, 2, 3, 4, 5, 10]", "Creating a list of numbers"),
            IPythonRunCellAction("print(f'Numbers: {numbers}')", "Displaying the numbers"),
            IPythonRunCellAction("squares = [x**2 for x in numbers]", "Calculating squares"),
            IPythonRunCellAction("print(f'Squares: {squares}')", "Displaying squares"),
            IPythonRunCellAction("factorial_10 = math.factorial(10)", "Calculating factorial of 10"),
            IPythonRunCellAction("print(f'10! = {factorial_10}')", "Displaying factorial result"),
            AgentFinishAction({"result": f"Completed mathematical calculations", "factorial_10": "3628800"})
        ]
    
    def _data_processing_script(self):
        return [
            IPythonRunCellAction("import csv", "Importing CSV module"),
            IPythonRunCellAction("""
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'San Francisco'],
    ['Charlie', 35, 'Chicago']
]
""", "Creating sample data"),
            IPythonRunCellAction("""
with open('sample_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
print('CSV file created successfully')
""", "Writing data to CSV file"),
            CmdRunAction("cat sample_data.csv", "Reading the CSV file"),
            IPythonRunCellAction("""
with open('sample_data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    print(f'Read {len(rows)} rows from CSV')
    for row in rows:
        print(row)
""", "Reading and processing CSV data"),
            AgentFinishAction({"result": "Successfully created and processed CSV data", "rows_processed": 4})
        ]
    
    def _general_demo_script(self):
        return [
            CmdRunAction("echo 'Starting Devin2 demo...'", "Starting the demo"),
            CmdRunAction("date", "Getting current date and time"),
            IPythonRunCellAction("print('Python is working!')", "Testing Python execution"),
            IPythonRunCellAction("import os; print(f'Working directory: {os.getcwd()}')", "Checking working directory"),
            CmdRunAction("echo 'Demo completed successfully!' > demo_result.txt", "Creating result file"),
            CmdRunAction("cat demo_result.txt", "Reading result file"),
            AgentFinishAction({"result": "Demo completed successfully"})
        ]
    
    async def step(self, state: State):
        """Execute the next step in the script."""
        if self.step_count >= len(self.script):
            return AgentFinishAction({"result": "Script completed"})
        
        action = self.script[self.step_count]
        self.step_count += 1
        
        return action


async def run_demo(task: str):
    """Run a demo with the given task."""
    print(f"🚀 Devin2 Demo: {task}")
    print("=" * 60)
    
    # Create config
    config = Config(
        model_name="demo",
        max_iterations=20,
        workspace_dir="/tmp/devin2_demo"
    )
    
    # Initialize components
    event_stream = EventStream("demo_session")
    runtime = Runtime(event_stream, config.workspace_dir)
    
    # Create demo agent
    agent = DemoAgent(task)
    
    # Initialize state
    initial_state = State(
        inputs={"task": task},
        max_iterations=config.max_iterations
    )
    
    # Initialize controller
    controller = AgentController(
        agent=agent,
        event_stream=event_stream,
        max_iterations=config.max_iterations,
        initial_state=initial_state
    )
    
    # Subscribe to events for logging
    def log_event(event):
        if hasattr(event, 'source'):
            source_icon = {
                EventSource.USER: "👤",
                EventSource.AGENT: "🤖", 
                EventSource.ENVIRONMENT: "🔧"
            }.get(event.source, "❓")
            
            event_type = event.__class__.__name__
            
            if hasattr(event, 'content') and event.content and event.content.strip():
                content = event.content[:100] + "..." if len(event.content) > 100 else event.content
                print(f"{source_icon} {content}")
            elif hasattr(event, 'command'):
                print(f"{source_icon} Executing: {event.command}")
            elif hasattr(event, 'code'):
                code_lines = event.code.strip().split('\n')
                if len(code_lines) == 1:
                    print(f"{source_icon} Python: {code_lines[0]}")
                else:
                    print(f"{source_icon} Python: {code_lines[0]}... ({len(code_lines)} lines)")
            elif hasattr(event, 'thought') and event.thought:
                print(f"{source_icon} {event.thought}")
    
    event_stream.subscribe("logger", log_event)
    
    try:
        # Start the agent
        await controller.start()
        
        # Send initial task message
        task_message = MessageAction(task)
        event_stream.add_event(task_message, EventSource.USER)
        
        # Wait for completion
        max_wait = 30  # seconds
        wait_count = 0
        while wait_count < max_wait:
            state = controller.get_state()
            if state.agent_state in [AgentState.FINISHED, AgentState.ERROR, AgentState.STOPPED]:
                break
            await asyncio.sleep(1)
            wait_count += 1
        
        # Get final results
        final_state = controller.get_state()
        
        print("\n" + "=" * 60)
        print("🏁 Demo Results:")
        print(f"📊 Status: {final_state.agent_state.value}")
        print(f"🔄 Steps completed: {final_state.iteration}")
        print(f"🎯 Result: {final_state.outputs}")
        
        if final_state.last_error:
            print(f"❌ Error: {final_state.last_error}")
        
        return final_state.agent_state == AgentState.FINISHED
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        await controller.stop()
        runtime.close()


async def main():
    """Run demo scenarios."""
    demos = [
        "Create a file with hello world",
        "Calculate factorial and squares using Python",
        "Create and process CSV data",
        "General system demo"
    ]
    
    print("🎭 Devin2 Demo Showcase")
    print("=" * 60)
    print("Available demos:")
    for i, demo in enumerate(demos, 1):
        print(f"  {i}. {demo}")
    
    if len(sys.argv) > 1:
        # Use command line argument
        task = " ".join(sys.argv[1:])
    else:
        # Interactive selection
        try:
            choice = input("\nEnter demo number (1-4) or custom task: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(demos):
                task = demos[int(choice) - 1]
            else:
                task = choice
        except (KeyboardInterrupt, EOFError):
            print("\nDemo cancelled.")
            return False
    
    print(f"\n🎬 Running demo: {task}")
    success = await run_demo(task)
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n💥 Demo failed!")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)