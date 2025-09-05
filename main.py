# main.py

import json
import uuid
from pprint import pprint
from langchain_core.messages import HumanMessage
from educational_agent_with_simulation.graph import graph

def main():
    """
    Main function to run the educational agent graph interactively.
    Uses LangGraph with checkpointing and interrupts for interactive learning.
    """
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}
    
    print("🎓 Educational Agent - Interactive Learning Session")
    print("=" * 50)
    print(f"Session ID: {session_id}")
    print("Type 'quit' or 'exit' to end the session")
    print("=" * 50)
    
    # Initialize the conversation with the graph
    try:
        # Start the graph - it will run until the first interrupt
        events = list(graph.stream({}, config=config))
        
        # Display the initial agent message
        for event in events:
            if isinstance(event, dict):
                for node_name, node_output in event.items():
                    if isinstance(node_output, dict) and node_output.get("agent_output"):
                        print(f"\nAgent [{node_name}]: {node_output['agent_output']}")
                        break
        
        # Main interaction loop
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! Session ended.")
                break
            
            if not user_input:
                print("Please enter a response or type 'quit' to exit.")
                continue
            
            try:
                # Update the graph state with user message
                graph.update_state(
                    config,
                    {"messages": [HumanMessage(content=user_input)]}
                )
                
                # Resume the graph execution (this is the key!)
                events = list(graph.stream(None, config=config))
                
                # Display agent response
                for event in events:
                    if isinstance(event, dict):
                        for node_name, node_output in event.items():
                            if isinstance(node_output, dict) and node_output.get("agent_output"):
                                print(f"\nAgent [{node_name}]: {node_output['agent_output']}")
                                break
                
            except Exception as e:
                print(f"\n❌ Error processing your input: {e}")
                print("Please try again or type 'quit' to exit.")
                continue
    
    except Exception as e:
        print(f"\n❌ Error starting the educational agent: {e}")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        return

def run_with_custom_config():
    """
    Alternative function to run with custom configuration.
    Useful for testing or specific session requirements.
    """
    
    # Custom configuration example
    custom_session_id = input("Enter custom session ID (or press Enter for auto-generated): ").strip()
    if not custom_session_id:
        custom_session_id = str(uuid.uuid4())
    
    config = {"configurable": {"thread_id": custom_session_id}}
    
    print(f"\n🔧 Starting custom session: {custom_session_id}")
    
    # You can add custom initial state here if needed
    initial_state = {}
    
    try:
        for event in graph.stream(initial_state, config=config):
            print(f"Event: {event}")
        print("✅ Custom session started successfully!")
        
    except Exception as e:
        print(f"❌ Error in custom session: {e}")

if __name__ == "__main__":
    main()
