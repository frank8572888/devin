import asyncio
import traceback
from typing import Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.state import State, AgentState
from events.stream import EventStream, EventSource
from events.action import Action, MessageAction, AgentFinishAction
from events.observation import Observation, ErrorObservation, AgentStateChangedObservation
from agent.base_agent import BaseAgent


class AgentController:
    """Controller for managing agent execution."""
    
    def __init__(
        self,
        agent: BaseAgent,
        event_stream: EventStream,
        max_iterations: int = 100,
        max_budget_per_task: Optional[float] = None,
        initial_state: Optional[State] = None
    ):
        self.agent = agent
        self.event_stream = event_stream
        self.max_iterations = max_iterations
        self.max_budget_per_task = max_budget_per_task
        
        # Initialize state
        if initial_state:
            self.state = initial_state
        else:
            self.state = State(max_iterations=max_iterations)
        
        # Subscribe to events
        self.event_stream.subscribe("agent_controller", self.on_event)
        
        # Task for running the agent loop
        self.agent_task: Optional[asyncio.Task] = None
        self._pending_action: Optional[Action] = None
        self._step_lock = asyncio.Lock()
    
    async def start(self):
        """Start the agent execution loop."""
        if self.agent_task is None:
            self.agent_task = asyncio.create_task(self._execution_loop())
    
    async def stop(self):
        """Stop the agent execution."""
        if self.agent_task:
            self.agent_task.cancel()
            try:
                await self.agent_task
            except asyncio.CancelledError:
                pass
        await self.set_agent_state(AgentState.STOPPED)
    
    async def on_event(self, event):
        """Handle incoming events."""
        if isinstance(event, MessageAction) and event.source == EventSource.USER:
            # User message received, resume if paused
            if self.state.agent_state != AgentState.RUNNING:
                await self.set_agent_state(AgentState.RUNNING)
        elif isinstance(event, Observation):
            # Handle observations from environment
            if self._pending_action and self._pending_action.id == event.cause:
                self.state.add_to_history(self._pending_action, event)
                self._pending_action = None
    
    async def set_agent_state(self, new_state: AgentState):
        """Set the agent state and notify subscribers."""
        if new_state != self.state.agent_state:
            self.state.agent_state = new_state
            observation = AgentStateChangedObservation("", new_state.value)
            self.event_stream.add_event(observation, EventSource.AGENT)
    
    async def _execution_loop(self):
        """Main execution loop for the agent."""
        await self.set_agent_state(AgentState.RUNNING)
        
        while True:
            try:
                await self._step()
                
                # Check termination conditions
                if self.state.agent_state in [
                    AgentState.FINISHED,
                    AgentState.ERROR,
                    AgentState.STOPPED
                ]:
                    break
                
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in execution loop: {e}")
                traceback.print_exc()
                await self.report_error(f"Unexpected error: {str(e)}")
                await self.set_agent_state(AgentState.ERROR)
                break
    
    async def _step(self):
        """Execute one step of the agent."""
        async with self._step_lock:
            # Check if we should continue
            if self.state.agent_state != AgentState.RUNNING:
                await asyncio.sleep(1)
                return
            
            # Check if we have a pending action
            if self._pending_action:
                await asyncio.sleep(0.5)
                return
            
            # Check iteration limit
            if self.state.iteration >= self.state.max_iterations:
                await self.report_error(f"Maximum iterations ({self.state.max_iterations}) reached")
                await self.set_agent_state(AgentState.FINISHED)
                return
            
            # Check budget limit
            if (self.max_budget_per_task and 
                self.state.metrics.accumulated_cost > self.max_budget_per_task):
                await self.report_error(f"Budget limit exceeded: ${self.state.metrics.accumulated_cost:.2f}")
                await self.set_agent_state(AgentState.FINISHED)
                return
            
            # Update iteration
            self.state.iteration += 1
            
            try:
                # Get next action from agent
                action = await self.agent.step(self.state)
                
                if action is None:
                    await self.report_error("Agent returned no action")
                    return
                
                # Handle the action
                if isinstance(action, AgentFinishAction):
                    self.state.outputs = action.outputs
                    await self.set_agent_state(AgentState.FINISHED)
                    return
                
                # If action is runnable, mark as pending
                if action.runnable:
                    self._pending_action = action
                else:
                    # Non-runnable actions (like messages) go directly to history
                    self.state.add_to_history(action, None)
                
                # Send action to event stream
                self.event_stream.add_event(action, EventSource.AGENT)
                
            except Exception as e:
                await self.report_error(f"Error in agent step: {str(e)}")
    
    async def report_error(self, message: str):
        """Report an error."""
        self.state.last_error = message
        error_obs = ErrorObservation(message)
        self.event_stream.add_event(error_obs, EventSource.AGENT)
        print(f"ERROR: {message}")
    
    def get_state(self) -> State:
        """Get the current state."""
        return self.state