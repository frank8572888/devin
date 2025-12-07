#!/usr/bin/env python3
"""
Test the full devin2 system with a mock agent (no LLM required).
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.state import State, AgentState
from events.stream import EventStream, EventSource
from events.action import MessageAction, CmdRunAction, IPythonRunCellAction, AgentFinishAction
from controller.agent_controller import AgentController
from agent.base_agent import BaseAgent
from runtime.runtime import Runtime


class MockAgent(BaseAgent):
    """A mock agent that follows a predefined script."""
    
    def __init__(self, name: str = "MockAgent"):
        super().__init__(name)
        self.step_count = 0
        self.script = [
            CmdRunAction("pwd", "Let me check the current directory"),
            CmdRunAction("echo 'Hello from Devin2!' > test_file.txt", "Creating a test file"),
            CmdRunAction("cat test_file.txt", "Reading the test file"),
            IPythonRunCellAction("print('Python is working!')", "Testing Python execution"),
            IPythonRunCellAction("import math; print(f'Square root of 16 is {math.sqrt(16)}')", "Testing math operations"),
            AgentFinishAction({"result": "Successfully tested bash and Python execution"}, "Task completed successfully")
        ]
    
    async def step(self, state: State):
        """Execute the next step in the script."""
        if self.step_count >= len(self.script):
            return AgentFinishAction({"result": "Script completed"})
        
        action = self.script[self.step_count]
        self.step_count += 1
        
        print(f"🤖 Mock Agent Step {self.step_count}: {action}")
        return action


async def test_full_system():
    """Test the complete devin2 system with mock agent."""
    print("🚀 Testing Full Devin2 System with Mock Agent")
    print("=" * 60)
    
    # Create config
    config = Config(
        model_name="mock",
        max_iterations=10,
        workspace_dir="/tmp/devin2_test_full"
    )
    
    # Initialize components
    event_stream = EventStream("test_full_session")
    runtime = Runtime(event_stream, config.workspace_dir)
    
    # Create mock agent
    agent = MockAgent()
    
    # Initialize state
    initial_state = State(
        inputs={"task": "Test bash and Python execution"},
        max_iterations=config.max_iterations
    )
    
    # Initialize controller
    controller = AgentController(
        agent=agent,
        event_stream=event_stream,
        max_iterations=config.max_iterations,
        initial_state=initial_state
    )
    
    # Subscribe to events for logging
    events_log = []
    def log_event(event):
        events_log.append(event)
        if hasattr(event, 'source'):
            source_icon = {
                EventSource.USER: "👤",
                EventSource.AGENT: "🤖", 
                EventSource.ENVIRONMENT: "🔧"
            }.get(event.source, "❓")
            
            event_type = event.__class__.__name__
            
            if hasattr(event, 'content') and event.content:
                content = event.content[:80] + "..." if len(event.content) > 80 else event.content
                print(f"   {source_icon} {event_type}: {content}")
            elif hasattr(event, 'command'):
                print(f"   {source_icon} {event_type}: {event.command}")
            elif hasattr(event, 'code'):
                code = event.code[:50] + "..." if len(event.code) > 50 else event.code
                print(f"   {source_icon} {event_type}: {code}")
            else:
                print(f"   {source_icon} {event_type}")
    
    event_stream.subscribe("logger", log_event)
    
    try:
        # Start the agent
        await controller.start()
        
        # Send initial task message
        task_message = MessageAction("Test bash and Python execution")
        event_stream.add_event(task_message, EventSource.USER)
        
        # Wait for completion
        max_wait = 30  # seconds
        wait_count = 0
        while wait_count < max_wait:
            state = controller.get_state()
            if state.agent_state in [AgentState.FINISHED, AgentState.ERROR, AgentState.STOPPED]:
                break
            await asyncio.sleep(1)
            wait_count += 1
        
        # Get final results
        final_state = controller.get_state()
        
        print("\n" + "=" * 60)
        print("🏁 Test Results:")
        print(f"   📊 Final state: {final_state.agent_state.value}")
        print(f"   🔄 Iterations: {final_state.iteration}")
        print(f"   🎯 Outputs: {final_state.outputs}")
        print(f"   📝 Events logged: {len(events_log)}")
        
        if final_state.last_error:
            print(f"   ❌ Last error: {final_state.last_error}")
        
        success = final_state.agent_state == AgentState.FINISHED
        print(f"   ✅ Success: {success}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        await controller.stop()
        runtime.close()


async def main():
    """Run the test."""
    success = await test_full_system()
    
    if success:
        print("\n🎉 Full system test passed!")
    else:
        print("\n💥 Full system test failed!")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)