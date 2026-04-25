"""
AI explanation layer for the music recommender.

Takes the top-k ranked songs from recommender.py and uses the Groq API
to generate a natural-language explanation of why each song was recommended.
Includes an output guardrail that validates the response before returning it.
"""

import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("recommender.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are a friendly music recommendation assistant. "
    "You will be given a user's taste profile and a ranked list of song recommendations "
    "produced by a scoring algorithm. Your job is to explain in plain, conversational English "
    "why each song was recommended, referencing the song's mood, energy level, genre, and "
    "acoustic qualities where relevant. Keep each explanation to 1-2 sentences. "
    "Only reference the songs provided — do not suggest others."
)


def _format_recommendations(user_prefs: dict, recommendations: list) -> str:
    lines = [
        f"User profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}",
        "",
        "Top recommended songs (ranked by score):",
    ]
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        lines.append(
            f"{i}. \"{song['title']}\" by {song['artist']} "
            f"(score: {score:.2f}/6.0) — {song['genre']}, {song['mood']} mood, "
            f"energy: {song['energy']:.2f}, acousticness: {song['acousticness']:.2f}"
        )
    return "\n".join(lines)


def _is_valid_response(text: str) -> bool:
    """Guardrail: check the response is usable before showing it to the user."""
    if not text or not text.strip():
        return False
    if len(text.strip()) < 40:
        return False
    if text.strip().startswith("Error") or text.strip().startswith("error"):
        return False
    return True


def explain_recommendations(user_prefs: dict, recommendations: list) -> str:
    """
    Call the Groq API to explain the recommendations in natural language.
    Returns the AI explanation, or falls back to the raw score output if the
    response fails the guardrail check.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY not set — using fallback output")
        return _fallback_output(recommendations)

    prompt = _format_recommendations(user_prefs, recommendations)
    logger.info("Sending recommendations to Groq for explanation...")

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=512,
            temperature=0.7,
        )
        result = response.choices[0].message.content
        logger.info("Received response from Groq (%d chars)", len(result))

        if not _is_valid_response(result):
            logger.warning("Response failed guardrail check — using fallback output")
            return _fallback_output(recommendations)

        return result

    except Exception as e:
        logger.error("Groq API call failed: %s", e)
        return _fallback_output(recommendations)


def _fallback_output(recommendations: list) -> str:
    """Raw score printout used when the AI response is unavailable or invalid."""
    lines = ["(AI explanation unavailable — showing raw scores)\n"]
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        lines.append(f"#{i}  {song['title']} by {song['artist']}")
        lines.append(f"    Score: {score:.2f}/6.0")
        for reason in explanation.split(" | "):
            lines.append(f"    + {reason}")
        lines.append("")
    return "\n".join(lines)