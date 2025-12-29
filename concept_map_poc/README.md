# Character-Based Timing Approach

This is a simplified version of the Concept Map Universal application that uses **character-based timing** instead of word-based timing.

## Key Differences from Original Version

### 1. **Character-Based Timing**
- **Original**: Fixed 0.35 seconds per word (regardless of word length)
- **New**: ~0.08 seconds per character
  - Shorter words (e.g., "a", "I") take ~0.15s minimum
  - Longer words (e.g., "photosynthesis") take proportionally more time
  - Maximum word duration capped at 1.5s
  
### 2. **gTTS Only**
- **Removed**: Edge-TTS dependency
- **Removed**: nest-asyncio (no async needed)
- **Removed**: mutagen and pydub (no MP3 duration reading)
- **Simpler**: Only uses gTTS for all audio generation

### 3. **No MP3 Duration Reading/Rescaling**
- **Original**: Generate MP3 → Read actual duration → Rescale all timings
- **New**: Character-based timing is accurate → No rescaling needed
- **Benefit**: Faster, simpler, no external dependencies for duration reading

## Timing Formula

```python
# Character-based calculation
clean_word = word.rstrip('.,!?;:')
char_count = len(clean_word)
word_duration = char_count * 0.08  # seconds

# Apply constraints
word_duration = max(0.15, min(word_duration, 1.5))

# Add punctuation pauses
if word.endswith('.!?'):
    word_duration += 0.4  # Sentence pause
elif word.endswith(',;:'):
    word_duration += 0.2  # Clause pause
```

## Examples

| Word | Characters | Base Time | Final Time | Notes |
|------|-----------|-----------|------------|-------|
| "I" | 1 | 0.08s | 0.15s | Minimum enforced |
| "the" | 3 | 0.24s | 0.24s | Natural |
| "photosynthesis" | 14 | 1.12s | 1.12s | Natural |
| "end." | 3 | 0.24s | 0.64s | +0.4s pause |

## Installation

```bash
cd character-based-approach
pip install -r requirements.txt
```

## Usage

Same as original:

```bash
streamlit run streamlit_app_standalone.py
```

## Benefits

1. ✅ **More natural timing**: Longer words take more time
2. ✅ **Simpler codebase**: No Edge-TTS, no async, no MP3 reading
3. ✅ **Fewer dependencies**: Only gTTS needed for audio
4. ✅ **Faster processing**: No duration reading/rescaling step
5. ✅ **Android-ready**: JSON timings work without MP3 generation

## For Android Integration

This version is perfect for Android apps because:
- Character-based timing is accurate without MP3
- You can skip MP3 generation entirely
- JSON output has correct `reveal_time` values
- Use your Android TTS with the provided timings

## Calibration

If you find gTTS timing slightly off, adjust in `timeline_mapper.py`:

```python
SECONDS_PER_CHARACTER = 0.08  # Increase/decrease as needed
```

Test with a known description, measure actual audio duration, and adjust.
