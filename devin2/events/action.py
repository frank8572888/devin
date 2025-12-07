from typing import Dict, Any, Optional
from .event import Event


class Action(Event):
    """Base class for all actions that can be performed by agents."""
    
    def __init__(self, thought: str = "", id: str = None):
        super().__init__(id)
        self.thought = thought
        self.runnable = True
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'thought': self.thought,
            'runnable': self.runnable
        })
        return result


class MessageAction(Action):
    """Action for sending messages."""
    
    def __init__(self, content: str, wait_for_response: bool = False, thought: str = "", id: str = None):
        super().__init__(thought, id)
        self.content = content
        self.wait_for_response = wait_for_response
        self.runnable = False
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'content': self.content,
            'wait_for_response': self.wait_for_response
        })
        return result
    
    def __str__(self) -> str:
        return f"MessageAction(content='{self.content[:50]}...')"


class CmdRunAction(Action):
    """Action for running shell commands."""
    
    def __init__(self, command: str, thought: str = "", id: str = None):
        super().__init__(thought, id)
        self.command = command
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'command': self.command
        })
        return result
    
    def __str__(self) -> str:
        return f"CmdRunAction(command='{self.command}')"


class IPythonRunCellAction(Action):
    """Action for running Python code in IPython."""
    
    def __init__(self, code: str, thought: str = "", id: str = None):
        super().__init__(thought, id)
        self.code = code
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'code': self.code
        })
        return result
    
    def __str__(self) -> str:
        return f"IPythonRunCellAction(code='{self.code[:50]}...')"


class AgentFinishAction(Action):
    """Action to indicate the agent has finished its task."""
    
    def __init__(self, outputs: Optional[Dict[str, Any]] = None, thought: str = "", id: str = None):
        super().__init__(thought, id)
        self.outputs = outputs or {}
        self.runnable = False
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'outputs': self.outputs
        })
        return result
    
    def __str__(self) -> str:
        return f"AgentFinishAction(outputs={self.outputs})"