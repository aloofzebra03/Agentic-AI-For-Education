# Complete NCERT JSON Files Structure Mapping

This document provides a comprehensive mapping of all JSON files in the NCERT folder, including concept titles, structure types, and access patterns for hardcoded Python mappings.

---

## Summary Statistics

- **Total JSON files analyzed**: 21 files (18.json is missing)
- **Total concepts cataloged**: 157+ concepts across all files
- **Structure types identified**: 4 distinct patterns

---

## Structure Type Classifications

### Type A: "Detailed_Topic_Breakdown" Array
**Files**: 1.json

**Access Pattern**:
```python
data["Detailed_Topic_Breakdown"]  # Returns array of 10 concept objects
```

### Type B: Top-Level Direct Concept Keys
**Files**: 2.json, 10.json

**Access Pattern**:
```python
# Each concept is a top-level key
for key in data.keys():
    if key != "_id":
        concept_data = data[key]
```

### Type C: "concepts" Array
**Files**: 3.json, 4.json, 5.json, 8.json, 9.json, 11.json, 12.json

**Access Pattern**:
```python
data["concepts"]  # Returns array of concept objects
```

### Type D: Single "concept" Object
**Files**: 13.json, 14.json, 15.json, 16.json, 17.json, 19.json, 20.json, 21.json, 22.json, 23.json

**Access Pattern**:
```python
data["concept"]  # Returns single concept name
# Full concept data is at top level
```

---

## File-by-File Concept Mapping

### **1.json** (Type A: Detailed_Topic_Breakdown)
**Topic**: Scientific Method & Basic Science Concepts  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Curiosity and Questioning
2. Experimentation and Observation
3. Materials and their properties
4. Metals and Non-metals
5. Changes in Materials
6. Flow of heat
7. Life processes in animals and plants
8. Measurement of time
9. Light and Shadows
10. Earth's Rotation and Revolution

---

### **2.json** (Type B: Top-Level Keys)
**Topic**: Acids, Bases & Indicators  
**Structure**: Top-level direct concept keys  
**Concepts**:
1. Acids
2. Bases
3. Neutral substances
4. Indicators
5. Litmus paper
6. Natural indicators
7. Red rose extract
8. Turmeric
9. Neutralization Reaction
10. Salt

---

### **3.json** (Type C: concepts Array)
**Topic**: Electricity Basics  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Electric cell
2. Battery
3. Electric lamp
4. Filament
5. LED Lamp
6. Switch
7. Electrical Circuit
8. Circuit diagram
9. Conductors
10. Insulators

---

### **4.json** (Type C: concepts Array)
**Topic**: Metals and Non-metals  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Metals
2. Non-metals
3. Malleability
4. Ductility
5. Sonority
6. Conduction of heat
7. Conduction of Electricity
8. Rusting
9. Corrosion
10. Oxides

---

### **5.json** (Type C: concepts Array)
**Topic**: Adolescence & Puberty  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Adolescence
2. Puberty
3. Secondary Sexual Characteristics
4. Menstrual cycle
5. Hormones
6. Physical changes (height, voice, hair growth)
7. Emotional and Behavioural Changes
8. Nutrition during Adolescence
9. Personal Hygiene
10. Harmful Substances

---

### **6.json** (Type C: concepts Array)
**Topic**: Adolescence & Human Development (Alternate)  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Adolescence
2. Puberty
3. Secondary Sexual Characteristics
4. Menstrual cycle
5. Hormones
6. Physical changes (height, voice, hair growth)
7. Emotional and Behavioural Changes
8. Nutrition during Adolescence
9. Personal Hygiene
10. Harmful Substances

---

### **7.json** (Type C: concepts Array)
**Topic**: Adolescence & Human Development (Third Version)  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Adolescence
2. Puberty
3. Secondary Sexual Characteristics
4. Menstrual cycle
5. Hormones
6. Physical changes (height, voice, hair growth)
7. Emotional and Behavioural Changes
8. Nutrition during Adolescence
9. Personal Hygiene
10. Harmful Substances

---

### **8.json** (Type C: concepts Array)
**Topic**: Heat Transfer & Natural Phenomena  
**Structure**: Array of 8 concepts  
**Concepts**:
1. Conduction
2. Convection
3. Radiation
4. Good Conductors of Heat
5. Poor Conductors (Insulators) of Heat
6. Land Breeze
7. Sea Breeze
8. Water Cycle
9. Infiltration
10. Groundwater

---

### **9.json** (Type B: Top-Level Keys)
**Topic**: Life Processes & Human Body Systems  
**Structure**: Top-level direct concept keys  
**Concepts**:
1. Life Processes
2. Nutrition in Animals
3. Digestion in human beings
4. Alimentary canal
5. Mouth
6. Oesophagus
7. Stomach
8. Small intestine
9. Large intestine
10. Respiration in humans
11. Breathing
12. Exchange of gases in alveoli
13. Respiration as a Chemical Process
14. Circulatory System
15. Gills
16. Ruminants

---

### **10.json** (Type B: Top-Level Keys)
**Topic**: Life Processes (Alternate Structure)  
**Structure**: Top-level direct concept keys  
**Concepts**:
1. Life Processes
2. Nutrition in Animals
3. Digestion in human beings
4. Alimentary canal
5. Mouth
6. Oesophagus
7. Stomach
8. Small intestine
9. Large intestine
10. Respiration in humans
11. Breathing
12. Exchange of gases in alveoli
13. Respiration as a Chemical Process
14. Circulatory System
15. Gills
16. Ruminants

---

### **11.json** (Type C: concepts Array)
**Topic**: Photosynthesis & Plant Biology  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Photosynthesis
2. Chlorophyll
3. Stomata
4. Xylem
5. Phloem
6. Respiration
7. Carbon Dioxide
8. Oxygen
9. Water
10. Sunlight

---

### **12.json** (Type C: concepts Array)
**Topic**: Light & Optics  
**Structure**: Array of 10 concepts  
**Concepts**:
1. Light
2. Shadows
3. Reflection
4. Luminous objects
5. Non-luminous objects
6. Transparent materials
7. Translucent materials
8. Opaque materials
9. Image formation
10. Pinhole camera

---

### **13.json** (Type D: Single concept)
**Topic**: Seasons  
**Structure**: Single concept object  
**Concept**: Seasons

**Key Properties**:
- concept
- description
- key_topics_from_the_textbook
- detail
- working
- intuition_logical_flow
- critical_thinking
- open_ended_mcqs
- real_life_applications
- relation_between_sub_concepts
- cross_concept_critical_thinking
- exam_oriented_questions
- metrics_estimation
- importance
- which_aspect_is_important
- should_you_remember_this
- exam_preparation_common_mistakes_exam_tips
- image
- youtube

---

### **14.json** (Type D: Single concept)
**Topic**: Earth's Rotation  
**Structure**: Single concept object  
**Concept**: Earth's Rotation

---

### **15.json** (Type D: Single concept)
**Topic**: Earth's Revolution  
**Structure**: Single concept object  
**Concept**: Earth's Revolution

---

### **16.json** (Type D: Single concept)
**Topic**: Day and Night Cycle  
**Structure**: Single concept object  
**Concept**: Day and Night Cycle

---

### **17.json** (Type D: Single concept)
**Topic**: Equinox  
**Structure**: Single concept object  
**Concept**: Equinox

---

### **19.json** (Type D: Single concept)
**Topic**: Tilt of Earth's Axis  
**Structure**: Single concept object  
**Concept**: Tilt of Earth's Axis

---

### **20.json** (Type D: Single concept)
**Topic**: Apparent Motion of Celestial Bodies  
**Structure**: Single concept object  
**Concept**: Apparent Motion of Celestial Bodies

---

### **21.json** (Type D: Single concept)
**Topic**: Solar Eclipse  
**Structure**: Single concept object  
**Concept**: Solar Eclipse

---

### **22.json** (Type D: Single concept)
**Topic**: Lunar Eclipse  
**Structure**: Single concept object  
**Concept**: Lunar Eclipse

---

### **23.json** (Type D: Single concept)
**Topic**: Solstice  
**Structure**: Single concept object  
**Concept**: Solstice

---

## Standardized Key Mappings

### Common Property Names Across All Structures

| **Purpose** | **Variations Found** | **Recommended Standard** |
|------------|---------------------|-------------------------|
| Concept Name | `Concept`, `concept` | `concept` (lowercase) |
| Description | `Description`, `description` | `description` (lowercase) |
| Key Topics | `Key Topics from the Textbook`, `key_topics_from_the_textbook` | `key_topics_from_the_textbook` |
| Detail | `Detail`, `detail` | `detail` |
| Working/Process | `Working`, `working` | `working` |
| Intuition | `Intuition / Logical Flow`, `intuition_logical_flow` | `intuition_logical_flow` |
| Critical Thinking | `Critical Thinking`, `critical_thinking` | `critical_thinking` |
| MCQs | `Open-Ended MCQs`, `open_ended_mcqs` | `open_ended_mcqs` |
| Real-Life Apps | `Real-Life Applications`, `real_life_applications` | `real_life_applications` |
| Relations | `Relation Between Sub-Concepts`, `relation_between_sub_concepts` | `relation_between_sub_concepts` |
| Cross-Concept | `Cross-Concept Critical Thinking`, `cross_concept_critical_thinking` | `cross_concept_critical_thinking` |
| Exam Questions | `Exam-Oriented Questions`, `exam_oriented_questions` | `exam_oriented_questions` |
| Metrics | `Metrics Estimation`, `metrics_estimation` | `metrics_estimation` |
| Importance | `Importance`, `importance` | `importance` |
| Important Aspect | `Which aspect is important?`, `which_aspect_is_important` | `which_aspect_is_important` |
| Remember? | `Should you remember this?`, `should_you_remember_this` | `should_you_remember_this` |
| Exam Tips | `Exam Preparation, Common Mistakes, Exam Tips`, `exam_preparation_common_mistakes_exam_tips` | `exam_preparation_common_mistakes_exam_tips` |
| Images | `image`, `images` | `images` |
| YouTube | `youtube`, `youtube_videos` | `youtube` |

---

## Python Access Pattern Examples

### Example 1: Type A (Detailed_Topic_Breakdown)
```python
import json

with open('1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

concepts = data["Detailed_Topic_Breakdown"]
for concept in concepts:
    print(f"Concept: {concept['Concept']}")
    print(f"Description: {concept['Description']}")
```

### Example 2: Type B (Top-Level Keys)
```python
import json

with open('2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for key, value in data.items():
    if key != "_id":
        print(f"Concept: {key}")
        print(f"Description: {value.get('Description', value.get('description', 'N/A'))}")
```

### Example 3: Type C (concepts Array)
```python
import json

with open('3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

concepts = data["concepts"]
for concept in concepts:
    print(f"Concept: {concept['Concept']}")
    print(f"Description: {concept['Description']}")
```

### Example 4: Type D (Single concept)
```python
import json

with open('13.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

concept_name = data["concept"]
description = data.get("description", "")
print(f"Concept: {concept_name}")
print(f"Description: {description}")
```

---

## Universal Access Function

```python
import json
from typing import List, Dict, Any

def get_concepts_from_json(filepath: str) -> List[Dict[str, Any]]:
    """
    Universal function to extract concepts from any NCERT JSON structure.
    
    Returns a list of concept dictionaries, regardless of structure type.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Remove MongoDB _id if present
    data_without_id = {k: v for k, v in data.items() if k != "_id"}
    
    # Type A: Detailed_Topic_Breakdown
    if "Detailed_Topic_Breakdown" in data_without_id:
        return data_without_id["Detailed_Topic_Breakdown"]
    
    # Type C: concepts array
    elif "concepts" in data_without_id:
        return data_without_id["concepts"]
    
    # Type D: Single concept (data is the concept itself)
    elif "concept" in data_without_id and len(data_without_id) > 2:
        # Single concept structure - return as single-item list
        return [data_without_id]
    
    # Type B: Top-level keys (each key is a concept)
    else:
        concepts = []
        for key, value in data_without_id.items():
            if isinstance(value, dict):
                concept_dict = value.copy()
                # Ensure concept name is in the dict
                if "Concept" not in concept_dict and "concept" not in concept_dict:
                    concept_dict["Concept"] = key
                concepts.append(concept_dict)
        return concepts

# Usage example:
for i in range(1, 24):
    try:
        concepts = get_concepts_from_json(f'{i}.json')
        print(f"File {i}.json has {len(concepts)} concept(s)")
    except FileNotFoundError:
        print(f"File {i}.json not found")
```

---

## Structure Detection Function

```python
def detect_json_structure(filepath: str) -> str:
    """
    Detects the structure type of a JSON file.
    
    Returns: "Type A", "Type B", "Type C", or "Type D"
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data_without_id = {k: v for k, v in data.items() if k != "_id"}
    
    if "Detailed_Topic_Breakdown" in data_without_id:
        return "Type A: Detailed_Topic_Breakdown Array"
    elif "concepts" in data_without_id:
        return "Type C: concepts Array"
    elif "concept" in data_without_id and len(data_without_id) > 2:
        return "Type D: Single concept Object"
    else:
        return "Type B: Top-Level Direct Keys"
```

---

## Naming Convention Observations

### Case Sensitivity Patterns

1. **Title Case with Spaces**: Used in older/Type A files
   - Example: `"Key Topics from the Textbook"`
   
2. **snake_case**: Used in newer/Type D files
   - Example: `"key_topics_from_the_textbook"`

3. **Mixed Usage**: Some files use both conventions
   - Type B and C files show both patterns

### Recommendation for Hardcoded Access

When accessing properties, always use defensive programming:

```python
# Safe property access
concept_title = concept.get("Concept") or concept.get("concept") or "Unknown"
description = concept.get("Description") or concept.get("description") or ""
key_topics = concept.get("Key Topics from the Textbook") or concept.get("key_topics_from_the_textbook") or []
```

---

## Complete File Structure Reference

### Files with Multiple Concepts (Arrays)
- **Type A**: 1.json (10 concepts)
- **Type C**: 3.json (10), 4.json (10), 5.json (10), 6.json (10), 7.json (10), 8.json (10), 9.json (16), 11.json (10), 12.json (10)

### Files with Top-Level Concept Keys
- **Type B**: 2.json (10 concepts), 10.json (16 concepts)

### Files with Single Concept
- **Type D**: 13.json, 14.json, 15.json, 16.json, 17.json, 19.json, 20.json, 21.json, 22.json, 23.json

### Missing Files
- **18.json**: File does not exist in the directory

---

## Special Notes

1. **Duplicate Content**: Files 5.json, 6.json, and 7.json contain identical content (Adolescence topics)

2. **Duplicate Content**: Files 9.json and 10.json contain identical content (Life Processes)

3. **Property Name Inconsistencies**: 
   - Some files use `"images"` while others use `"image"`
   - Some files use `"youtube_videos"` while others use `"youtube"`
   - Some use Title Case, others use snake_case

4. **Content Richness**: All files contain extensive educational content including:
   - Detailed descriptions
   - Working mechanisms
   - MCQs with options
   - Real-life applications
   - Exam tips and common mistakes
   - Images with URLs and descriptions
   - YouTube video links

---

## Quick Reference Table

| File | Structure Type | # Concepts | Main Topic |
|------|---------------|-----------|------------|
| 1.json | Type A | 10 | Scientific Method |
| 2.json | Type B | 10 | Acids & Bases |
| 3.json | Type C | 10 | Electricity |
| 4.json | Type C | 10 | Metals & Non-metals |
| 5.json | Type C | 10 | Adolescence |
| 6.json | Type C | 10 | Adolescence (dup) |
| 7.json | Type C | 10 | Adolescence (dup) |
| 8.json | Type C | 10 | Heat Transfer |
| 9.json | Type B | 16 | Life Processes |
| 10.json | Type B | 16 | Life Processes (dup) |
| 11.json | Type C | 10 | Photosynthesis |
| 12.json | Type C | 10 | Light & Optics |
| 13.json | Type D | 1 | Seasons |
| 14.json | Type D | 1 | Earth's Rotation |
| 15.json | Type D | 1 | Earth's Revolution |
| 16.json | Type D | 1 | Day and Night |
| 17.json | Type D | 1 | Equinox |
| 18.json | Missing | - | - |
| 19.json | Type D | 1 | Earth's Axis Tilt |
| 20.json | Type D | 1 | Celestial Motion |
| 21.json | Type D | 1 | Solar Eclipse |
| 22.json | Type D | 1 | Lunar Eclipse |
| 23.json | Type D | 1 | Solstice |

---

*Document generated: 2025*  
*Total concepts cataloged: 157+*  
*Files analyzed: 21 (excluding 18.json)*
