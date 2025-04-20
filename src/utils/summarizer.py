# src/utils/summarizer.py

import os
import logging

import openai

MAX_CHAR_COUNT = 250


def summarize_text(text: str, max_length: int = MAX_CHAR_COUNT) -> str:
    """
    Summarize a block of text to fit within max_length characters,
    falling back to simple truncation if no API key is present
    or if the OpenAI call fails.
    """
    if len(text) <= max_length:
        return text

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        logging.warning("⚠️ falling back to truncation")
        truncated = text[: max_length - 3].rstrip()
        return truncated + "..."

    openai.api_key = api_key
    try:
        system_prompt = (
            "You are a D&D assistant. Summarize the following spell description "
            f"into a single concise paragraph no more than {max_length} characters."
        )
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            max_tokens=int(max_length * 0.25),
        )
        summary = resp.choices[0].message.content.strip()

        if len(summary) > max_length:
            summary = summary[: max_length - 3].rstrip() + "..."
        return summary

    except Exception as e:
        logging.error(f"❌ OpenAI summarization failed: {e}")
        truncated = text[: max_length - 3].rstrip()
        return truncated + "..."
