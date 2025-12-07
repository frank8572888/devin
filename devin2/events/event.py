import uuid
from abc import ABC
from typing import Any, Dict


class Event(ABC):
    """Base class for all events in the system."""
    
    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())
        self.timestamp = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        return {
            'id': self.id,
            'type': self.__class__.__name__,
            'timestamp': self.timestamp
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"