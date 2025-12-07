import asyncio
from enum import Enum
from typing import Dict, List, Callable, Any
from .event import Event


class EventSource(Enum):
    """Source of events in the system."""
    USER = "user"
    AGENT = "agent"
    ENVIRONMENT = "environment"


class EventStream:
    """Event stream for managing events between components."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.events: List[Event] = []
        self.subscribers: Dict[str, Callable] = {}
    
    def add_event(self, event: Event, source: EventSource):
        """Add an event to the stream."""
        event.source = source
        self.events.append(event)
        
        # Notify subscribers
        for subscriber_id, callback in self.subscribers.items():
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(event))
                else:
                    callback(event)
            except Exception as e:
                print(f"Error in subscriber {subscriber_id}: {e}")
    
    def subscribe(self, subscriber_id: str, callback: Callable):
        """Subscribe to events."""
        self.subscribers[subscriber_id] = callback
    
    def unsubscribe(self, subscriber_id: str):
        """Unsubscribe from events."""
        if subscriber_id in self.subscribers:
            del self.subscribers[subscriber_id]
    
    def get_events(self) -> List[Event]:
        """Get all events in the stream."""
        return self.events.copy()
    
    def clear(self):
        """Clear all events."""
        self.events.clear()