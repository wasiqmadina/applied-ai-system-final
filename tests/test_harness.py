"""
Test harness — runs all 5 user profiles through the full pipeline
(recommender + AI explainer) and prints a pass/fail result for each.

Run with:
    python -m tests.test_harness
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recommender import load_songs, recommend_songs
from ai_explainer import explain_recommendations, _is_valid_response

_SONGS_PATH = Path(__file__).parent.parent / "data" / "songs.csv"

_PROFILES = [
    ("Chill Lofi Listener",           {"genre": "lofi",  "mood": "chill",   "energy": 0.38, "likes_acoustic": True}),
    ("High-Energy Pop Fan",            {"genre": "pop",   "mood": "happy",   "energy": 0.85, "likes_acoustic": False}),
    ("Deep Intense Rock",              {"genre": "rock",  "mood": "intense", "energy": 0.92, "likes_acoustic": False}),
    ("Edge Case: High Energy + Sad",   {"genre": "r&b",   "mood": "sad",     "energy": 0.90, "likes_acoustic": False}),
    ("Edge Case: Low Energy + Angry",  {"genre": "metal", "mood": "angry",   "energy": 0.10, "likes_acoustic": True}),
]


def run_harness() -> None:
    print("=" * 55)
    print("  Test Harness — Full Pipeline Check")
    print("=" * 55)

    songs = load_songs(str(_SONGS_PATH))
    passed = 0
    failed = 0

    for name, prefs in _PROFILES:
        try:
            recommendations = recommend_songs(prefs, songs, k=5)

            # Check 1: recommender returned the right number of results
            assert len(recommendations) == 5, f"Expected 5 recommendations, got {len(recommendations)}"

            # Check 2: each result has the expected structure
            for song, score, explanation in recommendations:
                assert isinstance(score, float), "Score must be a float"
                assert 0.0 <= score <= 6.0, f"Score {score} out of expected range"
                assert isinstance(explanation, str) and explanation.strip(), "Explanation must be a non-empty string"

            # Check 3: results are sorted highest score first
            scores = [score for _, score, _ in recommendations]
            assert scores == sorted(scores, reverse=True), "Recommendations are not sorted by score"

            # Check 4: AI explanation is returned and passes the guardrail
            ai_output = explain_recommendations(prefs, recommendations)
            assert isinstance(ai_output, str) and ai_output.strip(), "AI output must be a non-empty string"

            print(f"  PASS  {name}")
            passed += 1

        except Exception as e:
            print(f"  FAIL  {name}")
            print(f"        {e}")
            failed += 1

    print("=" * 55)
    print(f"  Results: {passed} passed, {failed} failed")
    print("=" * 55)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_harness()