# Quick Start - Character-Based Timing Version

## What's Different?

This version uses **character-based timing** where:
- Short words (e.g., "I") take ~0.15 seconds
- Long words (e.g., "photosynthesis") take ~1.12 seconds
- **No MP3 duration reading needed** - timings are accurate from the start
- **Only gTTS** - simplified dependencies

## Installation

```bash
cd /Users/imhvs0609/Desktop/Personal\ Education/character-based-approach
pip install -r requirements.txt
```

## Setup Environment Variables

Create a `.env` file:

```bash
# Required for LLM (Gemini)
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional for LangSmith tracking
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=concept-map-character-based
```

## Run the App

```bash
streamlit run streamlit_app_standalone.py
```

## How It Works

### 1. Character-Based Timing Formula

```python
# For each word
clean_word = word.rstrip('.,!?;:')  # Remove punctuation
char_count = len(clean_word)
base_duration = char_count * 0.08  # seconds per character

# Apply constraints
duration = max(0.15, min(base_duration, 1.5))

# Add punctuation pauses
if word.endswith('.!?'):
    duration += 0.4  # Period pause
elif word.endswith(',;:'):
    duration += 0.2  # Comma pause
```

### 2. Examples

| Word | Length | Base | Final | Reason |
|------|--------|------|-------|--------|
| "I" | 1 | 0.08s | 0.15s | Min enforced |
| "cat" | 3 | 0.24s | 0.24s | Natural |
| "incredible" | 10 | 0.80s | 0.80s | Natural |
| "photosynthesis" | 14 | 1.12s | 1.12s | Natural |
| "end." | 3 | 0.24s | 0.64s | +0.4s pause |

### 3. No Rescaling Needed

**Original Version:**
```
Calculate → Generate MP3 → Measure duration → Rescale all timings
```

**Character-Based Version:**
```
Calculate → Done! (Generate MP3 optional)
```

## For Android Integration

### Export JSON

The app generates a JSON file with this structure:

```json
{
  "metadata": {
    "total_duration": 32.5,
    "full_text": "Photosynthesis is..."
  },
  "concepts": [
    {
      "name": "Photosynthesis",
      "reveal_time": 2.45,
      "importance": 10
    },
    {
      "name": "Chloroplast",
      "reveal_time": 4.80,
      "importance": 9
    }
  ],
  "relationships": [
    {
      "source": "Photosynthesis",
      "target": "Chloroplast",
      "relationship": "occurs in"
    }
  ]
}
```

### Use in Android

1. Download the JSON from the app
2. Parse in Android: `val timeline = Gson().fromJson(json, Timeline::class.java)`
3. Use `reveal_time` values with your Android TTS
4. **No need for Python MP3** - character-based timings are accurate

### Android TTS Example

```kotlin
concepts.forEach { concept ->
    handler.postDelayed({
        revealConcept(concept.name)
    }, (concept.reveal_time * 1000).toLong())
}
```

## Calibration (If Needed)

If gTTS timing feels slightly off:

1. Generate a test description
2. Measure actual gTTS audio duration
3. Compare with JSON `total_duration`
4. Adjust in `timeline_mapper.py`:

```python
# Line ~176
SECONDS_PER_CHARACTER = 0.08  # Adjust this value
```

**Calibration Formula:**
```
new_rate = 0.08 × (actual_duration / estimated_duration)
```

**Example:**
- Estimated: 30.0s
- Actual: 33.0s  
- New rate: 0.08 × (33/30) = 0.088

## Troubleshooting

### Issue: Timing feels too fast

**Solution:** Increase `SECONDS_PER_CHARACTER`:
```python
SECONDS_PER_CHARACTER = 0.09  # or 0.10
```

### Issue: Timing feels too slow

**Solution:** Decrease `SECONDS_PER_CHARACTER`:
```python
SECONDS_PER_CHARACTER = 0.07  # or 0.06
```

### Issue: Short words too quick

**Solution:** Increase `MIN_WORD_DURATION`:
```python
MIN_WORD_DURATION = 0.20  # from 0.15
```

### Issue: Long words too slow

**Solution:** Decrease `MAX_WORD_DURATION`:
```python
MAX_WORD_DURATION = 1.0  # from 1.5
```

## Key Files Modified

- ✅ `timeline_mapper.py` - Character-based timing calculation
- ✅ `precompute_engine.py` - Simplified gTTS-only audio generation
- ✅ `requirements.txt` - Removed edge-tts, mutagen, pydub, nest-asyncio

## Advantages

1. ✅ **Natural timing** - Word length affects duration
2. ✅ **Simpler code** - 50% less audio code
3. ✅ **Fewer dependencies** - Only gTTS needed
4. ✅ **No async complexity** - Synchronous code only
5. ✅ **Android-ready** - JSON works without MP3
6. ✅ **Faster processing** - No duration reading step

## Next Steps

1. Test with your descriptions
2. Fine-tune `SECONDS_PER_CHARACTER` if needed
3. Export JSON for Android integration
4. Compare with your Android TTS timing

## Support

See these docs:
- `README.md` - Full overview
- `CHANGES_CHARACTER_BASED.md` - Detailed changes
- Original project docs - For other features
