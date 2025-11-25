"""
Comprehensive test suite for JSON mapping functionality.
Tests all concept titles and section keys across all JSON files.
"""

import json
import os
from utils.shared_utils import get_ground_truth_from_json, _build_concept_to_file_mapping

# Define test cases for each structure type
TEST_CASES = {
    "Structure 1 - Detailed_Topic_Breakdown (1.json)": {
        "concepts": ["Curiosity and Questioning", "Experimentation and Observation"],
        "sections": ["concept definition", "explanation (with analogies)", "details (facts, sub-concepts)", 
                    "working", "mcqs", "real-life application", "critical thinking"]
    },
    "Structure 2 - Top-Level Keys (2.json)": {
        "concepts": ["Acids", "Bases"],
        "sections": ["concept definition", "explanation (with analogies)", "details (facts, sub-concepts)", 
                    "working", "mcqs", "real-life application", "critical thinking"]
    },
    "Structure 3 - Concepts Array (3.json)": {
        "concepts": ["Electric cell", "Battery"],
        "sections": ["concept definition", "explanation (with analogies)", "details (facts, sub-concepts)", 
                    "working", "mcqs", "real-life application", "critical thinking"]
    },
    "Structure 4 - Single Top-Level Concept (10.json)": {
        "concepts": ["Life Processes"],
        "sections": ["concept definition", "explanation (with analogies)", "details (facts, sub-concepts)", 
                    "working", "mcqs", "real-life application", "critical thinking"]
    },
    "Structure 4 - Another Single Top-Level (15.json)": {
        "concepts": ["Earth's Revolution"],
        "sections": ["concept definition", "explanation (with analogies)", "details (facts, sub-concepts)", 
                    "working", "mcqs", "real-life application", "critical thinking"]
    }
}

def scan_all_concepts():
    """Scan all JSON files and extract all concept names."""
    print("\n" + "="*80)
    print("SCANNING ALL JSON FILES FOR CONCEPTS")
    print("="*80)
    
    ncert_dir = "NCERT"
    all_concepts = {}
    
    json_files = sorted([f for f in os.listdir(ncert_dir) if f.endswith('.json')])
    
    for json_file in json_files:
        file_path = os.path.join(ncert_dir, json_file)
        concepts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Structure 1: {"concepts": [{...}, ...]}
            if "concepts" in data and isinstance(data["concepts"], list):
                for concept_data in data["concepts"]:
                    concept_name = concept_data.get("concept", concept_data.get("Concept", ""))
                    if concept_name:
                        concepts.append(concept_name)
            
            # Structure 2: {"Detailed_Topic_Breakdown": [{...}, ...]}
            elif "Detailed_Topic_Breakdown" in data and isinstance(data["Detailed_Topic_Breakdown"], list):
                for concept_data in data["Detailed_Topic_Breakdown"]:
                    concept_name = concept_data.get("Concept", "")
                    if concept_name:
                        concepts.append(concept_name)
            
            # Structure 3: Top-level has single concept
            elif "concept" in data or "Concept" in data:
                concept_name = data.get("concept", data.get("Concept", ""))
                if concept_name:
                    concepts.append(concept_name)
            
            # Structure 4: Top-level keys are concepts
            else:
                for key in data.keys():
                    if key.startswith("_"):
                        continue
                    if isinstance(data[key], dict):
                        concept_name = data[key].get("Concept", data[key].get("concept", None))
                        if concept_name:
                            concepts.append(concept_name)
            
            all_concepts[json_file] = concepts
            print(f"✓ {json_file}: Found {len(concepts)} concept(s)")
            for concept in concepts[:3]:  # Show first 3
                print(f"    - {concept}")
            if len(concepts) > 3:
                print(f"    ... and {len(concepts) - 3} more")
                
        except Exception as e:
            print(f"✗ {json_file}: Error - {e}")
    
    return all_concepts

def test_concept_to_file_mapping():
    """Test that all concepts are correctly mapped to their files."""
    print("\n" + "="*80)
    print("TEST 1: CONCEPT TO FILE MAPPING")
    print("="*80)
    
    mapping = _build_concept_to_file_mapping()
    
    print(f"\n📊 Total concepts in mapping: {len(mapping)}")
    print("\nSample mappings:")
    for i, (concept, filepath) in enumerate(list(mapping.items())[:10]):
        print(f"  {i+1}. '{concept}' → {filepath}")
    
    return mapping

def test_section_retrieval(concept: str, section: str):
    """Test retrieval of a specific section for a concept."""
    try:
        result = get_ground_truth_from_json(concept, section)
        
        if result and not result.startswith("Concept") and not result.startswith("Section"):
            # Success - got actual content
            preview = result[:100].replace("\n", " ")
            return True, f"✓ Retrieved {len(result)} chars: {preview}..."
        else:
            # Got error message
            return False, f"✗ {result}"
    except Exception as e:
        return False, f"✗ Exception: {str(e)}"

def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("\n" + "="*80)
    print("COMPREHENSIVE JSON MAPPING TESTS")
    print("="*80)
    
    # Test 1: Scan all concepts
    all_concepts = scan_all_concepts()
    
    # Test 2: Concept-to-file mapping
    mapping = test_concept_to_file_mapping()
    
    # Test 3: Section retrieval for predefined test cases
    print("\n" + "="*80)
    print("TEST 2: SECTION RETRIEVAL FOR KEY CONCEPTS")
    print("="*80)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for structure_name, test_data in TEST_CASES.items():
        print(f"\n{'='*80}")
        print(f"{structure_name}")
        print(f"{'='*80}")
        
        for concept in test_data["concepts"]:
            print(f"\n📚 Testing Concept: '{concept}'")
            print("-" * 80)
            
            for section in test_data["sections"]:
                total_tests += 1
                success, message = test_section_retrieval(concept, section)
                
                if success:
                    passed_tests += 1
                    print(f"  {message}")
                else:
                    failed_tests.append({
                        "concept": concept,
                        "section": section,
                        "message": message
                    })
                    print(f"  {message}")
    
    # Test 4: Test "full" content retrieval
    print("\n" + "="*80)
    print("TEST 3: FULL CONTENT RETRIEVAL")
    print("="*80)
    
    test_concepts = ["Acids", "Electric cell", "Life Processes", "Earth's Revolution"]
    
    for concept in test_concepts:
        total_tests += 1
        success, message = test_section_retrieval(concept, "full")
        
        if success:
            passed_tests += 1
            print(f"  {concept}: {message}")
        else:
            failed_tests.append({
                "concept": concept,
                "section": "full",
                "message": message
            })
            print(f"  {concept}: {message}")
    
    # Test 5: Test with random concepts from each file
    print("\n" + "="*80)
    print("TEST 4: RANDOM SAMPLING FROM ALL FILES")
    print("="*80)
    
    for json_file, concepts in list(all_concepts.items())[:5]:  # Test first 5 files
        if concepts:
            concept = concepts[0]  # Test first concept from each file
            print(f"\n📂 {json_file} - Testing '{concept}'")
            
            test_sections = ["concept definition", "working", "mcqs"]
            for section in test_sections:
                total_tests += 1
                success, message = test_section_retrieval(concept, section)
                
                if success:
                    passed_tests += 1
                    print(f"  {message}")
                else:
                    failed_tests.append({
                        "concept": concept,
                        "section": section,
                        "message": message
                    })
                    print(f"  {message}")
    
    # Final Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ({100*passed_tests/total_tests:.1f}%)")
    print(f"Failed: {len(failed_tests)} ({100*len(failed_tests)/total_tests:.1f}%)")
    
    if failed_tests:
        print("\n" + "="*80)
        print("FAILED TESTS DETAILS")
        print("="*80)
        for i, failure in enumerate(failed_tests, 1):
            print(f"\n{i}. Concept: '{failure['concept']}'")
            print(f"   Section: '{failure['section']}'")
            print(f"   Error: {failure['message']}")
    
    # Test 6: Verify key variations work
    print("\n" + "="*80)
    print("TEST 5: KEY VARIATION TESTING")
    print("="*80)
    
    # Test that different key formats all map to the same content
    test_concept = "Acids"
    print(f"\n📚 Testing key variations for '{test_concept}'")
    
    # These should all return the same or similar content
    key_variations = [
        ("concept definition", "description"),
        ("explanation (with analogies)", "intuition"),
        ("details (facts, sub-concepts)", "detail"),
        ("real-life application", "applications"),
        ("critical thinking", "thinking")
    ]
    
    for section_name, expected_keyword in key_variations:
        success, message = test_section_retrieval(test_concept, section_name)
        print(f"  {section_name}: {message}")
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
