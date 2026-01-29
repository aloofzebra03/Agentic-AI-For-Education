"""Test script to verify language-based image filtering"""

from utils.shared_utils import select_most_relevant_image_for_concept_introduction

print("="*70)
print("🧪 TESTING LANGUAGE-BASED IMAGE SELECTION")
print("="*70)

# Test with a concept that has images with language metadata
test_concept = "Sources of Light: Luminous & Non-luminous"

print(f"\n📚 Testing concept: {test_concept}")
print("-"*70)

# Test 1: English language
print("\n1️⃣ Testing with English language:")
result_english = select_most_relevant_image_for_concept_introduction(
    concept=test_concept,
    definition_context="Luminous objects emit their own light, like the Sun.",
    language="English"
)
if result_english:
    print(f"   ✅ Found English image")
    print(f"   URL: {result_english.get('url', 'N/A')[:80]}...")
    print(f"   Language check: {'Kannada' in result_english.get('url', '') or 'kannada' in result_english.get('description', '').lower()}")
else:
    print(f"   ⚠️ No English image found")

# Test 2: Kannada language
print("\n2️⃣ Testing with Kannada language:")
result_kannada = select_most_relevant_image_for_concept_introduction(
    concept=test_concept,
    definition_context="Luminous objects emit their own light, like the Sun.",
    language="Kannada"
)
if result_kannada:
    print(f"   ✅ Found Kannada image")
    print(f"   URL: {result_kannada.get('url', 'N/A')[:80]}...")
    print(f"   Language check: {'Kannada' in result_kannada.get('url', '') or 'kannada' in result_kannada.get('description', '').lower()}")
else:
    print(f"   ⚠️ No Kannada image found")

# Test 3: Invalid language (should fallback to all images)
print("\n3️⃣ Testing with invalid language (should fallback):")
result_fallback = select_most_relevant_image_for_concept_introduction(
    concept=test_concept,
    definition_context="Luminous objects emit their own light, like the Sun.",
    language="Spanish"
)
if result_fallback:
    print(f"   ✅ Fallback worked - found an image")
    print(f"   URL: {result_fallback.get('url', 'N/A')[:80]}...")
else:
    print(f"   ⚠️ No fallback image found")

print("\n" + "="*70)
print("✅ LANGUAGE-BASED IMAGE FILTERING TEST COMPLETE")
print("="*70)
