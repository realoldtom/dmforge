"""Spell description summarizer utility."""

import logging

# Optional: import OpenAI if you plan to integrate directly
# import openai

MAX_CHAR_COUNT = 300  # Default max length for card descriptions


def summarize_text(text: str, max_length: int = MAX_CHAR_COUNT) -> str:
    """
    Summarize a block of text to fit within max_length characters.

    Args:
        text (str): Full original spell description
        max_length (int): Target character limit for the summary

    Returns:
        str: Summarized version of the text
    """
    if len(text) <= max_length:
        return text  # No need to summarize

    # Placeholder until LLM integration is active
    logging.warning("⚠️ Summarization placeholder used — description was too long")
    return text[: max_length - 3].rstrip() + "..."


# Optional: LLM-based summarization
# def summarize_with_openai(text: str, max_length: int) -> str:
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a D&D assistant. Summarize the following spell for a compact card format."
#             },
#             {
#                 "role": "user",
#                 "content": f"Summarize this spell in under {max_length} characters:\n\n{text}"
#             }
#         ]
#     )
#     return response.choices[0].message["content"].strip()
