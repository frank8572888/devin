"""
Devin2 - A simplified version of Devin AI agent

This package provides a streamlined implementation of an AI agent
that can execute bash commands and Python code to complete tasks.
"""

__version__ = "0.1.0"
__author__ = "Devin2 Team"

from .core.config import Config
from .core.state import State, AgentState
from .agent.simple_agent import SimpleAgent
from .agent.llm import LLM
from .controller.agent_controller import AgentController
from .runtime.runtime import Runtime
from .events.stream import EventStream

__all__ = [
    'Config',
    'State', 'AgentState',
    'SimpleAgent', 'LLM',
    'AgentController',
    'Runtime',
    'EventStream'
]