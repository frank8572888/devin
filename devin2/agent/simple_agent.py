import re
from typing import Optional, List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.base_agent import BaseAgent
from agent.llm import LLM
from core.state import State
from events.action import (
    Action, MessageAction, CmdRunAction, IPythonRunCellAction, AgentFinishAction
)


class SimpleAgent(BaseAgent):
    """A simple agent that can execute bash commands and Python code."""
    
    def __init__(self, llm: LLM, name: str = "SimpleAgent"):
        super().__init__(name)
        self.llm = llm
        
        self.system_prompt = """You are a helpful AI assistant that can execute bash commands and Python code to complete tasks.

You have access to the following tools:
1. <execute_bash>command</execute_bash> - Execute bash commands
2. <execute_ipython>code</execute_ipython> - Execute Python code
3. <finish>result</finish> - Finish the task with a result

Guidelines:
- Always think step by step
- Use bash commands for file operations, system tasks, and running programs
- Use Python for data processing, calculations, and complex logic
- Be careful with file paths and permissions
- Always verify your actions worked as expected
- When you complete the task, use <finish> with a summary of what you accomplished

Current working directory: You are in a workspace directory where you can create and modify files.

Example:
User: Create a file called hello.txt with "Hello World" and then read it back.

Response: I'll help you create a file with "Hello World" and then read it back.

<execute_bash>echo "Hello World" > hello.txt</execute_bash>

Now let me read the file back to verify it was created correctly:

<execute_bash>cat hello.txt</execute_bash>

<finish>Successfully created hello.txt with "Hello World" and verified its contents.</finish>"""
    
    async def step(self, state: State) -> Optional[Action]:
        """Take one step given the current state."""
        try:
            # Build conversation history
            messages = self._build_messages(state)
            
            # Get response from LLM
            response = await self.llm.complete(messages)
            
            # Parse the response for actions
            action = self._parse_response(response)
            
            return action
            
        except Exception as e:
            print(f"Error in agent step: {e}")
            return MessageAction(f"Error: {str(e)}")
    
    def _build_messages(self, state: State) -> List[Dict[str, str]]:
        """Build the conversation messages from state."""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add task from inputs if available
        if "task" in state.inputs:
            messages.append({"role": "user", "content": state.inputs["task"]})
        
        # Add history
        for item in state.get_recent_history(10):  # Last 10 interactions
            action = item.get('action')
            observation = item.get('observation')
            
            if action:
                if hasattr(action, 'content'):
                    messages.append({"role": "assistant", "content": action.content})
                elif hasattr(action, 'thought') and action.thought:
                    messages.append({"role": "assistant", "content": action.thought})
            
            if observation and hasattr(observation, 'content') and observation.content:
                messages.append({"role": "user", "content": f"Output: {observation.content}"})
        
        return messages
    
    def _parse_response(self, response: str) -> Optional[Action]:
        """Parse the LLM response to extract actions."""
        # Look for bash commands
        bash_match = re.search(r'<execute_bash>(.*?)</execute_bash>', response, re.DOTALL)
        if bash_match:
            command = bash_match.group(1).strip()
            thought = response[:bash_match.start()].strip()
            return CmdRunAction(command=command, thought=thought)
        
        # Look for Python code
        python_match = re.search(r'<execute_ipython>(.*?)</execute_ipython>', response, re.DOTALL)
        if python_match:
            code = python_match.group(1).strip()
            thought = response[:python_match.start()].strip()
            return IPythonRunCellAction(code=code, thought=thought)
        
        # Look for finish command
        finish_match = re.search(r'<finish>(.*?)</finish>', response, re.DOTALL)
        if finish_match:
            result = finish_match.group(1).strip()
            thought = response[:finish_match.start()].strip()
            return AgentFinishAction(outputs={"result": result}, thought=thought)
        
        # If no specific action found, treat as message
        return MessageAction(content=response)