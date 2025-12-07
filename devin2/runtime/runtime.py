import os
import subprocess
import asyncio
import sys
from typing import Dict, Any, Optional
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from events.stream import EventStream, EventSource
from events.action import CmdRunAction, IPythonRunCellAction
from events.observation import CmdOutputObservation, IPythonRunCellObservation, ErrorObservation


class Runtime:
    """Runtime environment for executing actions."""
    
    def __init__(self, event_stream: EventStream, workspace_dir: str = "/tmp/devin2_workspace"):
        self.event_stream = event_stream
        self.workspace_dir = workspace_dir
        self.python_globals = {}
        self.python_locals = {}
        
        # Create workspace directory
        os.makedirs(workspace_dir, exist_ok=True)
        os.chdir(workspace_dir)
        
        # Subscribe to action events
        self.event_stream.subscribe("runtime", self.handle_action)
    
    async def handle_action(self, event):
        """Handle incoming actions."""
        if isinstance(event, CmdRunAction):
            await self.execute_bash_command(event)
        elif isinstance(event, IPythonRunCellAction):
            await self.execute_python_code(event)
    
    async def execute_bash_command(self, action: CmdRunAction):
        """Execute a bash command."""
        try:
            # Change to workspace directory
            os.chdir(self.workspace_dir)
            
            # Execute command
            process = await asyncio.create_subprocess_shell(
                action.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=self.workspace_dir
            )
            
            stdout, _ = await process.communicate()
            output = stdout.decode('utf-8', errors='replace')
            exit_code = process.returncode
            
            # Create observation
            observation = CmdOutputObservation(
                content=output,
                command=action.command,
                exit_code=exit_code,
                cause=action.id
            )
            
            self.event_stream.add_event(observation, EventSource.ENVIRONMENT)
            
        except Exception as e:
            error_obs = ErrorObservation(
                content=f"Error executing command '{action.command}': {str(e)}",
                cause=action.id
            )
            self.event_stream.add_event(error_obs, EventSource.ENVIRONMENT)
    
    async def execute_python_code(self, action: IPythonRunCellAction):
        """Execute Python code."""
        try:
            # Capture stdout and stderr
            stdout_capture = StringIO()
            stderr_capture = StringIO()
            
            # Execute code
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                try:
                    # Try to compile and execute
                    compiled_code = compile(action.code, '<string>', 'exec')
                    exec(compiled_code, self.python_globals, self.python_locals)
                    
                    # If it's an expression, try to evaluate and print result
                    try:
                        result = eval(action.code, self.python_globals, self.python_locals)
                        if result is not None:
                            print(repr(result))
                    except:
                        pass  # Not an expression, that's fine
                        
                except SyntaxError:
                    # Try as expression
                    try:
                        result = eval(action.code, self.python_globals, self.python_locals)
                        if result is not None:
                            print(repr(result))
                    except Exception as e:
                        print(f"Error: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)
            
            # Get output
            stdout_content = stdout_capture.getvalue()
            stderr_content = stderr_capture.getvalue()
            
            output = ""
            if stdout_content:
                output += stdout_content
            if stderr_content:
                if output:
                    output += "\n"
                output += stderr_content
            
            # Create observation
            observation = IPythonRunCellObservation(
                content=output,
                code=action.code,
                cause=action.id
            )
            
            self.event_stream.add_event(observation, EventSource.ENVIRONMENT)
            
        except Exception as e:
            error_obs = ErrorObservation(
                content=f"Error executing Python code: {str(e)}",
                cause=action.id
            )
            self.event_stream.add_event(error_obs, EventSource.ENVIRONMENT)
    
    def close(self):
        """Clean up runtime resources."""
        self.event_stream.unsubscribe("runtime")