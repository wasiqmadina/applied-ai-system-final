"""
AI Music Recommender — runs all 5 user profiles through the recommendation
pipeline and prints a natural-language explanation for each using Groq AI.
"""

import sys
from pathlib import Path

# Ensure src/ is on the path regardless of how this script is invoked
sys.path.insert(0, str(Path(__file__).parent))

from recommender import load_songs, recommend_songs
from ai_explainer import explain_recommendations

_SONGS_PATH = Path(__file__).parent.parent / "data" / "songs.csv"

_PROFILES = [
    ("Chill Lofi Listener",           {"genre": "lofi",  "mood": "chill",   "energy": 0.38, "likes_acoustic": True}),
    ("High-Energy Pop Fan",            {"genre": "pop",   "mood": "happy",   "energy": 0.85, "likes_acoustic": False}),
    ("Deep Intense Rock",              {"genre": "rock",  "mood": "intense", "energy": 0.92, "likes_acoustic": False}),
    ("Edge Case: High Energy + Sad",   {"genre": "r&b",   "mood": "sad",     "energy": 0.90, "likes_acoustic": False}),
    ("Edge Case: Low Energy + Angry",  {"genre": "metal", "mood": "angry",   "energy": 0.10, "likes_acoustic": True}),
]


def run_profile(name: str, user_prefs: dict, songs: list) -> str:
    """Run one profile through the full pipeline and return the explanation."""
    recommendations = recommend_songs(user_prefs, songs, k=5)
    return explain_recommendations(user_prefs, recommendations)


def main() -> None:
    songs = load_songs(str(_SONGS_PATH))
    print(f"Loaded {len(songs)} songs\n")

    for name, prefs in _PROFILES:
        print("\n" + "=" * 55)
        print(f"  {name}")
        print(f"  Genre: {prefs['genre']} | Mood: {prefs['mood']} | Energy: {prefs['energy']}")
        print("=" * 55)
        explanation = run_profile(name, prefs, songs)
        print(explanation)

    print("\n" + "=" * 55)


if __name__ == "__main__":
    main()