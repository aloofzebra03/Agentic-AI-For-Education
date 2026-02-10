"""Helper functions for static autosuggestion generation.

This module provides pure helper functions for:
- Generating static autosuggestions based on node and state
- Translating suggestions to Kannada using cached translations
- Detecting suppression patterns in agent output
"""

import random
import re
from typing import Dict, List, Tuple, Optional

from utils.shared_utils import (
    POSITIVE_POOL,
    NEGATIVE_POOL,
    SPECIAL_HANDLING_POOL,
    translate_to_kannada_azure,
)

from .constants import (
    KANNADA_AUTOSUGGESTION_CACHE,
    NODE_SPECIAL_HANDLING,
    SUPPRESSION_PATTERNS,
)


def get_cached_kannada_translation(text: str) -> str:
    """Get Kannada translation from cache or Azure fallback.
    
    Args:
        text: English text to translate
        
    Returns:
        Kannada translation (from cache if available, otherwise from Azure)
    """
    if not text:
        return text
    
    # Check cache first for predefined suggestions
    if text in KANNADA_AUTOSUGGESTION_CACHE:
        print(f"✅ Using cached Kannada translation for: '{text}'")
        return KANNADA_AUTOSUGGESTION_CACHE[text]
    
    # Fall back to Azure for dynamic content
    print(f"🌐 No cache found, translating via Azure: '{text[:50]}...'")
    return translate_to_kannada_azure(text)


def should_suppress_positive(agent_output: str) -> bool:
    """Check if positive autosuggestion should be suppressed.
    
    Positive suggestions are suppressed when agent asks questions
    or uses thinking-aloud phrases like "let me think".
    
    Args:
        agent_output: The agent's output message
        
    Returns:
        True if positive suggestion should be None, False otherwise
    """
    if not agent_output:
        return False
    
    # Check against all suppression patterns
    for pattern in SUPPRESSION_PATTERNS:
        if re.search(pattern, agent_output, re.IGNORECASE):
            print(f"🚫 Suppressing positive suggestion (matched pattern: {pattern})")
            return True
    
    return False


def get_special_for_node(node: str) -> Optional[str]:
    """Get special handling suggestion for a specific node.
    
    Args:
        node: Current pedagogical node name (APK, CI, GE, AR, TC, RLC)
        
    Returns:
        Special handling suggestion string or None
    """
    special = NODE_SPECIAL_HANDLING.get(node)
    
    # Handle special "random" flag for GE node
    if special == "random":
        selected = random.choice(SPECIAL_HANDLING_POOL)
        print(f"🎲 GE node: randomly selected '{selected}' from special handling pool")
        return selected
    
    return special


def generate_static_autosuggestions(state, current_node: str) -> Tuple[List[str], Dict]:
    """Generate static autosuggestions for a pedagogical node.
    
    This is the main entry point called by pedagogical nodes to generate
    autosuggestions without LLM calls. All generation is static/rule-based.
    
    Args:
        state: AgentState dictionary
        current_node: Current node name (APK, CI, GE, AR, TC, RLC)
        
    Returns:
        Tuple of (final_suggestions_list, selections_dict)
        - final_suggestions_list: List of non-None suggestions to display
        - selections_dict: Dict with all 4 selection types (including None values)
    """
    agent_output = state.get("agent_output", "")
    is_kannada = state.get("is_kannada", False)
    
    # ─── Generate Positive Suggestion ─────────────────────────────────────
    # Suppress if agent asks question or says "let me think"
    if should_suppress_positive(agent_output):
        positive = None
    else:
        # Randomly select from positive pool (excluding None at end)
        positive = random.choice(POSITIVE_POOL[:-1])
    
    # ─── Generate Negative Suggestion ─────────────────────────────────────
    # Always present - randomly select from negative pool
    negative = random.choice(NEGATIVE_POOL)
    
    # ─── Generate Special Handling Suggestion ────────────────────────────
    # Node-specific logic from NODE_SPECIAL_HANDLING mapping
    special = get_special_for_node(current_node)
    
    # ─── Dynamic Suggestion ───────────────────────────────────────────────
    # Always None for static implementation (no LLM generation)
    dynamic = None
    
    # ─── Create Selections Dictionary ────────────────────────────────────
    selections_dict = {
        'positive': positive,
        'negative': negative,
        'special': special,
        'dynamic': dynamic
    }
    
    # ─── Translate to Kannada if Needed ───────────────────────────────────
    if is_kannada:
        print("🌐 Translating autosuggestions to Kannada (using cache for predefined suggestions)...")
        selections_dict = {
            k: get_cached_kannada_translation(v) if v and isinstance(v, str) else v
            for k, v in selections_dict.items()
        }
    
    # ─── Create Final Suggestions List ───────────────────────────────────
    # Filter out None values for display
    final_suggestions = [s for s in [
        selections_dict['positive'],
        selections_dict['negative'],
        selections_dict['special'],
        selections_dict['dynamic']
    ] if s]
    
    print("=" * 80)
    print(f"📋 STATIC AUTOSUGGESTIONS GENERATED FOR {current_node}")
    print("=" * 80)
    print(f"✅ Positive: {positive}")
    print(f"❌ Negative: {negative}")
    print(f"⚙️  Special:  {special}")
    print(f"🔮 Dynamic:  {dynamic}")
    print(f"📤 Final List ({len(final_suggestions)}): {final_suggestions}")
    print("=" * 80)
    
    return final_suggestions, selections_dict
