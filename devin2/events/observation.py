from typing import Dict, Any, Optional
from .event import Event


class Observation(Event):
    """Base class for all observations from the environment."""
    
    def __init__(self, content: str = "", cause: str = None, id: str = None):
        super().__init__(id)
        self.content = content
        self.cause = cause  # ID of the action that caused this observation
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'content': self.content,
            'cause': self.cause
        })
        return result


class CmdOutputObservation(Observation):
    """Observation from command execution."""
    
    def __init__(self, content: str, command_id: int = -1, command: str = "", 
                 exit_code: int = 0, cause: str = None, id: str = None):
        super().__init__(content, cause, id)
        self.command_id = command_id
        self.command = command
        self.exit_code = exit_code
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'command_id': self.command_id,
            'command': self.command,
            'exit_code': self.exit_code
        })
        return result
    
    def __str__(self) -> str:
        return f"CmdOutputObservation(command='{self.command}', exit_code={self.exit_code})"


class IPythonRunCellObservation(Observation):
    """Observation from IPython code execution."""
    
    def __init__(self, content: str, code: str = "", cause: str = None, id: str = None):
        super().__init__(content, cause, id)
        self.code = code
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'code': self.code
        })
        return result
    
    def __str__(self) -> str:
        return f"IPythonRunCellObservation(code='{self.code[:50]}...')"


class ErrorObservation(Observation):
    """Observation for errors that occur during execution."""
    
    def __init__(self, content: str, cause: str = None, id: str = None):
        super().__init__(content, cause, id)
    
    def __str__(self) -> str:
        return f"ErrorObservation(content='{self.content}')"


class AgentStateChangedObservation(Observation):
    """Observation for when agent state changes."""
    
    def __init__(self, content: str, agent_state: str, cause: str = None, id: str = None):
        super().__init__(content, cause, id)
        self.agent_state = agent_state
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result.update({
            'agent_state': self.agent_state
        })
        return result
    
    def __str__(self) -> str:
        return f"AgentStateChangedObservation(agent_state='{self.agent_state}')"