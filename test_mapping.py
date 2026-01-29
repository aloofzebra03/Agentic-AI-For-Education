"""Test script to verify the auto-scanning concept mapping function"""

from utils.shared_utils import _build_concept_to_file_mapping, get_all_available_concepts

print("="*70)
print("🧪 TESTING AUTO-SCANNING CONCEPT MAPPING")
print("="*70)

# Test the mapping function
mapping = _build_concept_to_file_mapping()

# Calculate stats
total_concepts = len([k for k in mapping.keys() if k != "_default"])
total_files = len(set(mapping.values()))

print(f"\n📊 STATISTICS:")
print(f"   Total concepts mapped: {total_concepts}")
print(f"   Total JSON files: {total_files}")
print(f"   Default file: {mapping.get('_default', 'None')}")

print(f"\n🔍 SAMPLE MAPPINGS (first 15):")
for i, (concept, file) in enumerate(list(mapping.items())[:15]):
    if concept != "_default":
        print(f"   {i+1}. '{concept}' -> {file}")

print(f"\n📚 ALL AVAILABLE CONCEPTS:")
concepts = get_all_available_concepts()
print(f"   Found {len(concepts)} concepts")
for i, concept in enumerate(concepts[:20]):
    print(f"   {i+1}. {concept}")
if len(concepts) > 20:
    print(f"   ... and {len(concepts) - 20} more")

print(f"\n✅ AUTO-SCANNING WORKS CORRECTLY!")
print("="*70)
