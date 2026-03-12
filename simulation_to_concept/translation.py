"""
Translation Module
==================
Provides English ↔ Kannada translation for the teaching agent API.

Uses deep-translator (wraps Google Translate, free, no API key needed).
Translation is applied at the API boundary only — the internal LangGraph
pipeline always operates in English for consistent evaluation quality.

Features:
- In-memory caching to avoid re-translating identical strings
- Batch translation for efficiency (concept lists, quiz questions)
- Graceful fallback to original text on translation failure
"""

from typing import Dict, List, Optional, Tuple
from deep_translator import GoogleTranslator
import traceback
import concurrent.futures

# Timeout (seconds) for each Google Translate HTTP request.
# Prevents Streamlit from hanging when Google rate-limits or is slow.
_TRANSLATE_TIMEOUT_SECONDS = 8


# ═══════════════════════════════════════════════════════════════════════
# SUPPORTED LANGUAGES
# ═══════════════════════════════════════════════════════════════════════

SUPPORTED_LANGUAGES = {
    "english": "en",
    "kannada": "kn",
}

DEFAULT_LANGUAGE = "english"


# ═══════════════════════════════════════════════════════════════════════
# TRANSLATION CACHE
# ═══════════════════════════════════════════════════════════════════════

# In-memory cache: (text, source_lang, target_lang) -> translated_text
_translation_cache: Dict[Tuple[str, str, str], str] = {}


def _get_cached(text: str, source: str, target: str) -> Optional[str]:
    """Check cache for existing translation."""
    return _translation_cache.get((text, source, target))


def _set_cached(text: str, source: str, target: str, translated: str):
    """Store translation in cache."""
    _translation_cache[(text, source, target)] = translated


def clear_cache():
    """Clear the translation cache (useful for testing)."""
    _translation_cache.clear()


def get_cache_stats() -> Dict[str, int]:
    """Get cache statistics."""
    return {"cached_translations": len(_translation_cache)}


# ═══════════════════════════════════════════════════════════════════════
# CORE TRANSLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def translate(text: str, source: str = "en", target: str = "kn") -> str:
    """
    Translate text between languages using Google Translate (via deep-translator).
    
    Args:
        text: The text to translate
        source: Source language code ('en', 'kn')
        target: Target language code ('en', 'kn')
        
    Returns:
        Translated text, or original text if translation fails
    """
    # Skip if source == target or text is empty
    if source == target or not text or not text.strip():
        return text
    
    # Check cache first
    cached = _get_cached(text, source, target)
    if cached is not None:
        return cached
    
    try:
        translator = GoogleTranslator(source=source, target=target)
        
        # Run in thread with timeout to avoid hanging when Google rate-limits.
        # IMPORTANT: do NOT use ThreadPoolExecutor as a context manager here —
        # executor.__exit__ calls shutdown(wait=True), which blocks until the
        # worker thread finishes, negating the timeout entirely.
        # Instead, call shutdown(wait=False) so the timeout is real.
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(translator.translate, text)
        executor.shutdown(wait=False)
        try:
            translated = future.result(timeout=_TRANSLATE_TIMEOUT_SECONDS)
        except concurrent.futures.TimeoutError:
            print(f"[TRANSLATE] Timeout ({_TRANSLATE_TIMEOUT_SECONDS}s) translating: {text[:50]}... — returning original")
            return text
        
        if translated:
            _set_cached(text, source, target, translated)
            return translated
        else:
            print(f"[TRANSLATE] Warning: Empty translation result for text: {text[:50]}...")
            return text
            
    except Exception as e:
        print(f"[TRANSLATE] Error translating text: {e}")
        traceback.print_exc()
        return text  # Graceful fallback to original


def translate_to_english(text: str) -> str:
    """Translate Kannada text to English."""
    return translate(text, source="kn", target="en")


def translate_to_kannada(text: str) -> str:
    """Translate English text to Kannada."""
    return translate(text, source="en", target="kn")


def translate_batch(texts: List[str], source: str = "en", target: str = "kn") -> List[str]:
    """
    Translate a list of texts in parallel for efficiency.

    Cache hits are resolved instantly; only uncached strings hit the network.
    All uncached strings are translated concurrently (one thread per string)
    so the total wall-clock time equals the slowest single call, not the sum.

    Args:
        texts: List of texts to translate
        source: Source language code
        target: Target language code

    Returns:
        List of translated texts (same order as input)
    """
    if source == target:
        return texts

    results: List[Optional[str]] = [None] * len(texts)

    # Resolve cache hits immediately; collect indices that need network calls
    uncached_indices = []
    for i, text in enumerate(texts):
        cached = _get_cached(text, source, target)
        if cached is not None:
            results[i] = cached
        else:
            uncached_indices.append(i)

    if not uncached_indices:
        return results  # type: ignore[return-value]

    # Translate all uncached strings in parallel
    def _translate_one(idx: int) -> tuple:
        text = texts[idx]
        if not text or not text.strip():
            return idx, text
        try:
            translator = GoogleTranslator(source=source, target=target)
            translated = translator.translate(text)
            if translated:
                _set_cached(text, source, target, translated)
                return idx, translated
        except Exception as e:
            print(f"[TRANSLATE] Parallel translate error for '{text[:40]}...': {e}")
        return idx, text  # fallback: return original

    max_workers = min(len(uncached_indices), 10)  # cap at 10 parallel threads
    # Do NOT use `with ThreadPoolExecutor` here — its __exit__ calls shutdown(wait=True)
    # which blocks until every thread finishes, negating the timeout entirely.
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    futures = {pool.submit(_translate_one, i): i for i in uncached_indices}
    pool.shutdown(wait=False)  # detach — threads keep running but we won't block on them
    try:
        completed = concurrent.futures.as_completed(futures, timeout=_TRANSLATE_TIMEOUT_SECONDS + 2)
        for future in completed:
            try:
                idx, translated = future.result()
                results[idx] = translated
            except Exception as e:
                orig_idx = futures[future]
                print(f"[TRANSLATE] Future error at index {orig_idx}: {e}")
                results[orig_idx] = texts[orig_idx]  # fallback
    except concurrent.futures.TimeoutError:
        print(f"[TRANSLATE] Batch timeout — using results collected so far, falling back for unfinished futures.")
        for future, orig_idx in futures.items():
            if results[orig_idx] is None:
                if future.done():
                    try:
                        idx, translated = future.result()
                        results[orig_idx] = translated
                    except Exception:
                        results[orig_idx] = texts[orig_idx]
                else:
                    results[orig_idx] = texts[orig_idx]  # not done — use original

    # Fill any None slots (shouldn't happen, but be safe)
    for i, r in enumerate(results):
        if r is None:
            results[i] = texts[i]

    return results  # type: ignore[return-value]


# ═══════════════════════════════════════════════════════════════════════
# LANGUAGE VALIDATION
# ═══════════════════════════════════════════════════════════════════════

def is_supported_language(language: str) -> bool:
    """Check if a language is supported."""
    return language.lower() in SUPPORTED_LANGUAGES


def get_language_code(language: str) -> str:
    """
    Get the ISO language code for a supported language name.
    
    Args:
        language: Language name (e.g., 'english', 'kannada')
        
    Returns:
        Language code (e.g., 'en', 'kn')
        
    Raises:
        ValueError: If language is not supported
    """
    lang_lower = language.lower()
    if lang_lower not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language: '{language}'. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        )
    return SUPPORTED_LANGUAGES[lang_lower]


def needs_translation(language: str) -> bool:
    """
    Check if translation is needed (i.e., language is not English).
    
    Args:
        language: Language name (e.g., 'english', 'kannada')
        
    Returns:
        True if translation is required, False for English
    """
    return language.lower() != "english"


# ═══════════════════════════════════════════════════════════════════════
# API RESPONSE TRANSLATION
# ═══════════════════════════════════════════════════════════════════════

def translate_api_response(response: Dict, language: str) -> Dict:
    """
    Translate all user-facing text in an API response to the target language.
    
    Translates:
    - teacher_message.text (the main LLM-generated message)
    - concepts.current_concept fields (title, description, key_insight)
    - concepts.all_concepts list (title, description, key_insight for each)
    - summary (if present)
    
    Does NOT translate:
    - IDs, timestamps, URLs, parameter names/values
    - Internal state fields (strategy, understanding_level, etc.)
    
    Args:
        response: The formatted API response dict
        language: Target language (e.g., 'kannada')
        
    Returns:
        Response dict with translated text fields
    """
    if not needs_translation(language):
        return response
    
    target = get_language_code(language)
    
    print(f"[TRANSLATE] Translating API response to {language} ({target})")
    
    # 1. Translate teacher message
    if "teacher_message" in response and response["teacher_message"].get("text"):
        original_text = response["teacher_message"]["text"]
        response["teacher_message"]["text"] = translate(original_text, source="en", target=target)
    
    # 2. Translate current concept
    if "concepts" in response:
        current = response["concepts"].get("current_concept")
        if current:
            for field in ["title", "description", "key_insight"]:
                if current.get(field):
                    current[field] = translate(current[field], source="en", target=target)
        
        # 3. Translate all concepts list
        for concept in response["concepts"].get("all_concepts", []):
            for field in ["title", "description", "key_insight"]:
                if concept.get(field):
                    concept[field] = translate(concept[field], source="en", target=target)
        
        # 4. Translate previous concept title if present
        prev = response["concepts"].get("previous_concept")
        if prev and prev.get("title"):
            prev["title"] = translate(prev["title"], source="en", target=target)
    
    # 5. Translate simulation title
    if "simulation" in response and response["simulation"].get("title"):
        response["simulation"]["title"] = translate(
            response["simulation"]["title"], source="en", target=target
        )
    
    # 6. Translate param change reason
    if ("simulation" in response 
        and response["simulation"].get("param_change")
        and response["simulation"]["param_change"].get("reason")):
        response["simulation"]["param_change"]["reason"] = translate(
            response["simulation"]["param_change"]["reason"], source="en", target=target
        )
    
    # 7. Translate summary if present
    if response.get("summary"):
        # Summary is mostly numeric, but translate any text fields
        pass  # Summary fields are numeric — no translation needed
    
    # Add language indicator to response
    response["language"] = language
    
    return response


def translate_quiz_response(response: Dict, language: str) -> Dict:
    """
    Translate user-facing text in a quiz evaluation response.
    
    Translates:
    - feedback (LLM-generated adaptive feedback)
    - next_question.challenge (quiz question text)
    
    Args:
        response: The quiz evaluation response dict
        language: Target language (e.g., 'kannada')
        
    Returns:
        Response dict with translated text fields
    """
    if not needs_translation(language):
        return response
    
    target = get_language_code(language)
    
    print(f"[TRANSLATE] Translating quiz response to {language} ({target})")
    
    # 1. Translate feedback
    if response.get("feedback"):
        response["feedback"] = translate(response["feedback"], source="en", target=target)
    
    # 2. Translate next question challenge text
    if response.get("next_question") and response["next_question"].get("challenge"):
        response["next_question"]["challenge"] = translate(
            response["next_question"]["challenge"], source="en", target=target
        )
    
    # Add language indicator
    response["language"] = language
    
    return response


def translate_student_input(text: str, language: str) -> str:
    """
    Translate student input to English for internal processing.
    
    Args:
        text: Student's input text (possibly in Kannada)
        language: Session language (e.g., 'kannada')
        
    Returns:
        English translation of the input, or original if already English
    """
    if not needs_translation(language):
        return text
    
    source = get_language_code(language)
    translated = translate(text, source=source, target="en")
    print(f"[TRANSLATE] Student input: '{text[:50]}...' → '{translated[:50]}...'")
    return translated
