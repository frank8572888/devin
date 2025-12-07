#!/usr/bin/env python3
"""
Basic test of devin2 components without requiring API keys.
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules directly
import core.state as state_module
import events.stream as stream_module
import events.action as action_module
import runtime.runtime as runtime_module

State = state_module.State
AgentState = state_module.AgentState
EventStream = stream_module.EventStream
EventSource = stream_module.EventSource
MessageAction = action_module.MessageAction
CmdRunAction = action_module.CmdRunAction
IPythonRunCellAction = action_module.IPythonRunCellAction
Runtime = runtime_module.Runtime


async def test_basic_components():
    """Test basic components without LLM."""
    print("🧪 Testing basic components...")
    
    # Test state
    print("✅ Testing State...")
    state = State()
    assert state.agent_state == AgentState.INIT
    assert state.iteration == 0
    print(f"   State: {state.to_dict()}")
    
    # Test event stream
    print("✅ Testing EventStream...")
    event_stream = EventStream("test_session")
    
    events_received = []
    def event_handler(event):
        events_received.append(event)
    
    event_stream.subscribe("test", event_handler)
    
    # Test message action
    msg_action = MessageAction("Hello, world!")
    event_stream.add_event(msg_action, EventSource.USER)
    
    assert len(events_received) == 1
    assert events_received[0].content == "Hello, world!"
    print(f"   Event received: {events_received[0]}")
    
    # Test runtime
    print("✅ Testing Runtime...")
    runtime = Runtime(event_stream, "/tmp/devin2_test")
    
    # Test bash command
    cmd_action = CmdRunAction("echo 'Hello from bash'")
    await runtime.execute_bash_command(cmd_action)
    
    # Test Python code
    python_action = IPythonRunCellAction("print('Hello from Python')")
    await runtime.execute_python_code(python_action)
    
    # Wait a bit for async operations
    await asyncio.sleep(0.5)
    
    runtime.close()
    
    print("✅ All basic tests passed!")
    return True


async def test_mock_agent_loop():
    """Test a mock agent execution loop."""
    print("\n🤖 Testing mock agent loop...")
    
    event_stream = EventStream("mock_session")
    runtime = Runtime(event_stream, "/tmp/devin2_mock_test")
    
    # Mock agent actions
    actions = [
        CmdRunAction("pwd"),
        CmdRunAction("ls -la"),
        IPythonRunCellAction("import os; print(f'Current dir: {os.getcwd()}')"),
        CmdRunAction("echo 'Task completed' > result.txt"),
        CmdRunAction("cat result.txt")
    ]
    
    print("   Executing mock agent actions...")
    for i, action in enumerate(actions):
        print(f"   Step {i+1}: {action}")
        event_stream.add_event(action, EventSource.AGENT)
        await asyncio.sleep(0.2)  # Small delay between actions
    
    # Wait for all actions to complete
    await asyncio.sleep(1)
    
    runtime.close()
    print("✅ Mock agent loop completed!")
    return True


async def main():
    """Run all tests."""
    print("🚀 Starting Devin2 Basic Tests")
    print("=" * 50)
    
    try:
        await test_basic_components()
        await test_mock_agent_loop()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)