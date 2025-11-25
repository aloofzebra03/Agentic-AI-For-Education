"""Quick test of JSON mapping functionality"""
import sys
sys.path.insert(0, 'c:\\Users\\aryan\\Desktop\\Personalized_Education\\Agentic-AI-For-Education')

from utils.shared_utils import get_ground_truth_from_json, _build_concept_to_file_mapping

print("="*80)
print("QUICK JSON MAPPING TEST")
print("="*80)

# Test 1: Build mapping
print("\n1. Building concept-to-file mapping...")
mapping = _build_concept_to_file_mapping()
print(f"   Found {len(mapping)} concepts")

# Test 2: Test specific concepts from different structures
test_cases = [
    ("Acids", "concept definition"),
    ("Acids", "working"),
    ("Electric cell", "concept definition"),
    ("Life Processes", "concept definition"),
    ("Earth's Revolution", "concept definition"),
]

print("\n2. Testing specific concept/section pairs...")
for concept, section in test_cases:
    result = get_ground_truth_from_json(concept, section)
    if result and len(result) > 50 and not result.startswith("Concept") and not result.startswith("Section"):
        print(f"   ✓ {concept} / {section}: Got {len(result)} chars")
    else:
        print(f"   ✗ {concept} / {section}: {result[:100]}")

print("\n" + "="*80)
print("TEST COMPLETED")
print("="*80)
