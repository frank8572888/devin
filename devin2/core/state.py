from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class AgentState(Enum):
    """Possible states of the agent."""
    INIT = "init"
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"
    ERROR = "error"
    STOPPED = "stopped"
    AWAITING_USER_INPUT = "awaiting_user_input"


@dataclass
class Metrics:
    """Metrics for tracking agent performance."""
    accumulated_cost: float = 0.0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0


@dataclass
class State:
    """State of the agent and its environment."""
    
    # Core state
    agent_state: AgentState = AgentState.INIT
    iteration: int = 0
    max_iterations: int = 100
    
    # Task and inputs
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    
    # History and memory
    history: List[Any] = field(default_factory=list)
    
    # Metrics
    metrics: Metrics = field(default_factory=Metrics)
    
    # Error tracking
    last_error: Optional[str] = None
    
    def add_to_history(self, action, observation):
        """Add action-observation pair to history."""
        self.history.append({
            'action': action,
            'observation': observation,
            'iteration': self.iteration
        })
    
    def get_recent_history(self, n: int = 10) -> List[Any]:
        """Get the most recent n history items."""
        return self.history[-n:] if self.history else []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            'agent_state': self.agent_state.value,
            'iteration': self.iteration,
            'max_iterations': self.max_iterations,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'history_length': len(self.history),
            'metrics': {
                'accumulated_cost': self.metrics.accumulated_cost,
                'total_tokens': self.metrics.total_tokens,
                'prompt_tokens': self.metrics.prompt_tokens,
                'completion_tokens': self.metrics.completion_tokens
            },
            'last_error': self.last_error
        }