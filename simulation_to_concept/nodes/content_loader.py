"""
Content Loader Node
===================
Loads pre-defined concepts from configuration.

This node runs ONCE at the start of a session to:
1. Load pre-defined concepts (no LLM extraction needed)
2. Set up the teaching sequence
3. Pass constraints (cannot_demonstrate) to state
"""

from typing import Dict, Any

from simulation_to_concept.config import PRE_DEFINED_CONCEPTS, CANNOT_DEMONSTRATE, TOPIC_TITLE


def content_loader_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load pre-defined concepts for teaching.
    
    Input State:
        - topic_description: The source material (for reference)
        
    Output State:
        - concepts: List of pre-defined Concept objects
        - cannot_demonstrate: List of topics to avoid
        
    Note: This is much simpler than LLM-based extraction and ensures
    consistent, reliable concept teaching.
    """
    print("\n" + "="*60)
    print("📚 CONTENT LOADER: Loading pre-defined concepts")
    print("="*60)
    
    # Load pre-defined concepts (no LLM needed!)
    concepts = PRE_DEFINED_CONCEPTS
    
    print(f"\n✅ Loaded {len(concepts)} concepts for '{TOPIC_TITLE}':")
    for c in concepts:
        print(f"   {c['id']}. {c['title']}")
        print(f"      Key insight: {c['key_insight']}")
        print(f"      Params: {c['related_params']}")
    
    print(f"\n⚠️ Topics NOT in this simulation (will not mention):")
    for item in CANNOT_DEMONSTRATE:
        print(f"   - {item}")
    
    return {
        "concepts": concepts,
        "current_concept_index": 0,
        "cannot_demonstrate": CANNOT_DEMONSTRATE
    }
