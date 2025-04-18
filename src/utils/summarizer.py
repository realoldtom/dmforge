# src/utils/summarizer.py

import os
import logging
import openai

# Character limit for card descriptions
MAX_CHAR_COUNT = 300

# Load your OpenAI API key (make sure you’ve exported OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY", "")


def summarize_text(text: str, max_length: int = MAX_CHAR_COUNT) -> str:
    """
    Summarize a block of text to fit within max_length characters.
    Uses OpenAI if API key is set, otherwise does a simple truncation.
    """
    # If it already fits, return as‑is
    if len(text) <= max_length:
        return text

    # If no key, warn and truncate
    if not openai.api_key:
        logging.warning("⚠️ OPENAI_API_KEY not set — falling back to truncation")
        return text[: max_length - 3].rstrip() + "..."

    try:
        # Build system prompt
        system_prompt = (
            "You are a D&D assistant. "
            f"Summarize the following spell description into a single concise paragraph "
            f"no more than {max_length} characters, preserving key mechanical details."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            # rough token estimate: 4 chars ~ 1 token
            max_tokens=int(max_length * 0.25),
        )

        summary = response.choices[0].message.content.strip()

        # Ensure final length
        if len(summary) > max_length:
            summary = summary[: max_length - 3].rstrip() + "..."
        return summary

    except Exception as e:
        logging.error(f"❌ OpenAI summarization failed: {e}")
        # fallback to truncation
        return text[: max_length - 3].rstrip() + "..."
