# question_bank.py
"""
Simple question bank loader for the revision agent.
Just handles loading JSON files - all other logic is in the nodes.
"""

import json
import os
from typing import Dict, Any

def load_question_bank(chapter_name: str) -> Dict[str, Any]:
    """
    Load question bank from JSON file.
    
    Args:
        chapter_name: Name of the chapter (e.g., "Nutrition in Plants", "ch1")
    
    Returns:
        Dict containing chapter name and list of questions
    """
    # Normalize chapter name to filename
    filename = chapter_name.lower().replace(" ", "_")
    if not filename.endswith(".json"):
        filename += ".json"
    
    filepath = os.path.join("revision_agent", "question_banks", filename)
    
    print(f"📚 Loading question bank from: {filepath}")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Question bank not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get("questions", [])
    print(f"✅ Loaded {len(questions)} questions for chapter: {data.get('chapter', chapter_name)}")
    
    return data
