#!/usr/bin/env python3
"""
Devin2 - A simplified version of Devin AI agent
Main entry point for running the agent with a task.
"""

import asyncio
import argparse
import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.state import State, AgentState
from events.stream import EventStream, EventSource
from events.action import MessageAction
from controller.agent_controller import AgentController
from agent.llm import LLM
from agent.simple_agent import SimpleAgent
from runtime.runtime import Runtime


class Devin2:
    """Main Devin2 application."""
    
    def __init__(self, config: Config):
        self.config = config
        self.event_stream = EventStream("main_session")
        self.runtime: Optional[Runtime] = None
        self.controller: Optional[AgentController] = None
        
    async def run_task(self, task: str) -> dict:
        """Run a task with the agent."""
        print(f"🚀 Starting Devin2 with task: {task}")
        print(f"📁 Workspace: {self.config.workspace_dir}")
        print(f"🤖 Model: {self.config.model_name}")
        print("-" * 50)
        
        try:
            # Initialize LLM
            llm = LLM(
                model=self.config.model_name,
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
            
            # Initialize agent
            agent = SimpleAgent(llm=llm)
            
            # Initialize runtime
            self.runtime = Runtime(
                event_stream=self.event_stream,
                workspace_dir=self.config.workspace_dir
            )
            
            # Initialize state with task
            initial_state = State(
                inputs={"task": task},
                max_iterations=self.config.max_iterations
            )
            
            # Initialize controller
            self.controller = AgentController(
                agent=agent,
                event_stream=self.event_stream,
                max_iterations=self.config.max_iterations,
                max_budget_per_task=self.config.max_budget_per_task,
                initial_state=initial_state
            )
            
            # Subscribe to events for logging
            self.event_stream.subscribe("logger", self._log_event)
            
            # Start the agent
            await self.controller.start()
            
            # Send initial task message
            task_message = MessageAction(content=task)
            self.event_stream.add_event(task_message, EventSource.USER)
            
            # Wait for completion
            while True:
                state = self.controller.get_state()
                if state.agent_state in [AgentState.FINISHED, AgentState.ERROR, AgentState.STOPPED]:
                    break
                await asyncio.sleep(1)
            
            # Get final results
            final_state = self.controller.get_state()
            
            print("\n" + "=" * 50)
            print("🏁 Task completed!")
            print(f"📊 Final state: {final_state.agent_state.value}")
            print(f"🔄 Iterations: {final_state.iteration}")
            print(f"💰 Cost: ${final_state.metrics.accumulated_cost:.4f}")
            print(f"🎯 Outputs: {final_state.outputs}")
            
            if final_state.last_error:
                print(f"❌ Last error: {final_state.last_error}")
            
            return {
                "success": final_state.agent_state == AgentState.FINISHED,
                "state": final_state.agent_state.value,
                "outputs": final_state.outputs,
                "iterations": final_state.iteration,
                "cost": final_state.metrics.accumulated_cost,
                "error": final_state.last_error
            }
            
        except Exception as e:
            print(f"❌ Error running task: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # Cleanup
            if self.controller:
                await self.controller.stop()
            if self.runtime:
                self.runtime.close()
    
    async def _log_event(self, event):
        """Log events for debugging."""
        if hasattr(event, 'source'):
            source_icon = {
                EventSource.USER: "👤",
                EventSource.AGENT: "🤖", 
                EventSource.ENVIRONMENT: "🔧"
            }.get(event.source, "❓")
            
            event_type = event.__class__.__name__
            
            if hasattr(event, 'content') and event.content:
                content = event.content[:100] + "..." if len(event.content) > 100 else event.content
                print(f"{source_icon} {event_type}: {content}")
            elif hasattr(event, 'command'):
                print(f"{source_icon} {event_type}: {event.command}")
            elif hasattr(event, 'code'):
                code = event.code[:50] + "..." if len(event.code) > 50 else event.code
                print(f"{source_icon} {event_type}: {code}")
            else:
                print(f"{source_icon} {event_type}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Devin2 - Simplified AI Agent")
    parser.add_argument("task", help="Task for the agent to complete")
    parser.add_argument("--model", default="gpt-4", help="LLM model to use")
    parser.add_argument("--max-iterations", type=int, default=100, help="Maximum iterations")
    parser.add_argument("--workspace", default="/tmp/devin2_workspace", help="Workspace directory")
    parser.add_argument("--api-key", help="API key for LLM")
    parser.add_argument("--base-url", help="Base URL for LLM API")
    
    args = parser.parse_args()
    
    # Create config
    config = Config(
        model_name=args.model,
        api_key=args.api_key or os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY'),
        base_url=args.base_url,
        max_iterations=args.max_iterations,
        workspace_dir=args.workspace
    )
    
    if not config.api_key:
        print("❌ Error: No API key provided. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable, or use --api-key")
        sys.exit(1)
    
    # Run the task
    devin2 = Devin2(config)
    result = await devin2.run_task(args.task)
    
    # Exit with appropriate code
    sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    asyncio.run(main())