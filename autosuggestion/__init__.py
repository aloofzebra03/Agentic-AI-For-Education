"""Autosuggestion module for educational agent.

Provides static autosuggestion generation, handler functions,
and manager nodes for the pedagogical flow.
"""

from .helpers import generate_static_autosuggestions
from .nodes import autosuggestion_manager_node, pause_for_handler

__all__ = [
    'generate_static_autosuggestions',
    'autosuggestion_manager_node',
    'pause_for_handler',
]
