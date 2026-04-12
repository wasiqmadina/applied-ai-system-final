from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return (score out of 6.0, list of reason strings)."""
    score = 0.0
    reasons = []

    # mood match — worth up to 2.0 points (binary)
    if song["mood"] == user_prefs["mood"]:
        score += 2.0
        reasons.append(f"mood match: '{song['mood']}' (+2.0)")

    # energy fit — worth up to 3.0 points (doubled from 1.5 to make energy more decisive)
    energy_fit = 3.0 * (1.0 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_fit
    reasons.append(f"energy fit: {energy_fit:.2f}/3.0 (song={song['energy']}, target={user_prefs['energy']})")

    # genre match — worth up to 0.5 points (halved from 1.0 — genre is a preference not a dealbreaker)
    if song["genre"] == user_prefs["genre"]:
        score += 0.5
        reasons.append(f"genre match: '{song['genre']}' (+0.5)")

    # acoustic fit — worth up to 0.5 points (continuous)
    if user_prefs["likes_acoustic"]:
        acoustic_fit = 0.5 * song["acousticness"]
    else:
        acoustic_fit = 0.5 * (1.0 - song["acousticness"])
    score += acoustic_fit
    reasons.append(f"acoustic fit: {acoustic_fit:.2f}/0.5 (acousticness={song['acousticness']})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
