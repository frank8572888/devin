from abc import ABC, abstractmethod
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.state import State
from events.action import Action


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, name: str = "BaseAgent"):
        self.name = name
    
    @abstractmethod
    async def step(self, state: State) -> Optional[Action]:
        """
        Take one step given the current state.
        
        Args:
            state: Current state of the environment
            
        Returns:
            Action to take, or None if no action
        """
        pass
    
    def reset(self):
        """Reset the agent to initial state."""
        pass