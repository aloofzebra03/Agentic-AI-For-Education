"""
Manual verification of JSON mappings by directly checking files
"""
import json
import os

os.chdir('c:\\Users\\aryan\\Desktop\\Personalized_Education\\Agentic-AI-For-Education')

print("="*80)
print("MANUAL JSON STRUCTURE VERIFICATION")
print("="*80)

# Check each JSON file structure
test_files = [
    ("NCERT/1.json", "Curiosity and Questioning"),
    ("NCERT/2.json", "Acids"),
    ("NCERT/3.json", "Electric cell"),
    ("NCERT/10.json", "Life Processes"),
    ("NCERT/15.json", "Earth's Revolution"),
]

for filepath, expected_concept in test_files:
    print(f"\n{'='*80}")
    print(f"File: {filepath}")
    print(f"Expected concept: {expected_concept}")
    print("="*80)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Identify structure
        if "Detailed_Topic_Breakdown" in data:
            print("✓ Structure: Detailed_Topic_Breakdown array")
            concepts = [c.get("Concept") for c in data["Detailed_Topic_Breakdown"]]
            print(f"  Found {len(concepts)} concepts")
            print(f"  Concepts: {concepts[:3]}")
            
            # Check keys in first concept
            if concepts:
                sample = data["Detailed_Topic_Breakdown"][0]
                print(f"  Keys: {list(sample.keys())[:8]}")
                
        elif "concepts" in data and isinstance(data["concepts"], list):
            print("✓ Structure: concepts array")
            concepts = [c.get("Concept", c.get("concept")) for c in data["concepts"]]
            print(f"  Found {len(concepts)} concepts")
            print(f"  Concepts: {concepts[:3]}")
            
            # Check keys
            if concepts:
                sample = data["concepts"][0]
                print(f"  Keys: {list(sample.keys())[:8]}")
                
        elif "concept" in data or "Concept" in data:
            print("✓ Structure: Single top-level concept")
            concept = data.get("concept", data.get("Concept"))
            print(f"  Concept: {concept}")
            print(f"  Keys: {[k for k in data.keys() if not k.startswith('_')][:8]}")
            
        else:
            print("✓ Structure: Top-level concept keys")
            concepts = []
            for key in data.keys():
                if not key.startswith("_") and isinstance(data[key], dict):
                    concept = data[key].get("Concept", data[key].get("concept", key))
                    concepts.append(concept)
            print(f"  Found {len(concepts)} concepts")
            print(f"  Concepts: {concepts[:3]}")
            
            # Check keys in first concept
            if concepts:
                first_key = [k for k in data.keys() if not k.startswith("_")][0]
                sample = data[first_key]
                print(f"  Keys in '{first_key}': {list(sample.keys())[:8]}")
        
        # Test specific section key retrieval
        print("\n  Testing key existence:")
        test_keys = [
            "description", "Description",
            "detail", "Detail",
            "working", "Working",
            "intuition_logical_flow", "Intuition_Logical_Flow", "Intuition / Logical Flow",
            "open_ended_mcqs", "Open-Ended_MCQs", "Open-Ended MCQs"
        ]
        
        # Get sample concept data
        if "Detailed_Topic_Breakdown" in data:
            sample = data["Detailed_Topic_Breakdown"][0]
        elif "concepts" in data:
            sample = data["concepts"][0]
        elif "concept" in data or "Concept" in data:
            sample = data
        else:
            first_key = [k for k in data.keys() if not k.startswith("_")][0]
            sample = data[first_key]
        
        found_keys = []
        for key in test_keys:
            if key in sample:
                found_keys.append(key)
        
        print(f"  Found keys: {found_keys}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "="*80)
print("VERIFICATION COMPLETED")
print("="*80)
