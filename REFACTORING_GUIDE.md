# Shared Utilities Refactoring

## Overview

This refactoring extracts common helper functions from `nodes4_rag_studio.py` into a shared utilities module to enable code reuse between the traditional educational agent and the new simulation-based agent.

## Files Created/Modified

### New Files:
- `educational_agent/shared_utils.py` - Contains all shared helper functions
- `educational_agent/__init__.py` - Package initialization
- `educational_agent_with_simulation/__init__.py` - Package initialization

### Modified Files:
- `educational_agent/nodes4_rag_studio.py` - Now imports from shared_utils
- `educational_agent_with_simulation/simulation_nodes.py` - Now uses shared utilities

## Extracted Functions

The following functions were moved to `shared_utils.py`:

1. **Core Utilities:**
   - `extract_json_block()` - JSON extraction from LLM responses
   - `get_llm()` - LLM instance configuration
   - `add_ai_message_to_conversation()` - Message management
   - `llm_with_history()` - LLM invocation with context

2. **Prompt Management:**
   - `build_conversation_history()` - Format conversation for prompts
   - `build_prompt_from_template()` - Template-based prompt building

3. **Content Retrieval:**
   - `get_ground_truth()` - RAG-based content retrieval

4. **Configuration:**
   - `PEDAGOGICAL_MOVES` - Shared pedagogical strategies
   - `AgentState` - Type alias for state management

## Benefits

1. **DRY Principle**: No code duplication between agents
2. **Maintainability**: Single source of truth for common functions
3. **Consistency**: Same behavior across all agents
4. **Modularity**: Clear separation between shared utilities and agent-specific logic
5. **Safe Refactoring**: Original agent remains untouched and deployable

## Usage Example

```python
# In any node file
from educational_agent.shared_utils import (
    AgentState,
    add_ai_message_to_conversation,
    llm_with_history,
    build_prompt_from_template,
    PEDAGOGICAL_MOVES
)

def my_node(state: AgentState) -> AgentState:
    # Use shared utilities
    prompt = build_prompt_from_template(
        system_prompt="Your prompt here",
        state=state,
        include_last_message=True
    )
    
    response = llm_with_history(state, prompt)
    add_ai_message_to_conversation(state, response.content)
    
    return state
```

## Design Principles Applied

- **Single Responsibility**: Each function has one clear purpose
- **Open/Closed**: Easy to extend without modifying existing code
- **Dependency Inversion**: Nodes depend on abstractions (shared utilities)
- **Don't Repeat Yourself**: Eliminated code duplication
- **Separation of Concerns**: Clear boundaries between utilities and business logic
