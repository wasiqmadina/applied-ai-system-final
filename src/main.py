"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # User taste profile — defines what kind of song this user is looking for
    user_prefs = {
        "genre": "lofi",        # preferred musical style
        "mood": "chill",        # emotional tone the user wants
        "energy": 0.38,         # target intensity level (0.0 = very calm, 1.0 = very intense)
        "likes_acoustic": True, # prefers acoustic/organic sound over electronic
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Top Recommendations")
    print(f"  Genre: {user_prefs['genre']} | Mood: {user_prefs['mood']} | Energy: {user_prefs['energy']}")
    print("=" * 50)

    for i, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 6.0")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"      + {reason}")

    print("\n" + "=" * 50)

    # --- Profile 2: High-Energy Pop ---
    profile2 = {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False}
    recs2 = recommend_songs(profile2, songs, k=5)
    print("\n" + "=" * 50)
    print("  High-Energy Pop Fan")
    print(f"  Genre: {profile2['genre']} | Mood: {profile2['mood']} | Energy: {profile2['energy']}")
    print("=" * 50)
    for i, rec in enumerate(recs2, start=1):
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 6.0")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        for reason in explanation.split(" | "):
            print(f"      + {reason}")
    print("\n" + "=" * 50)

    # --- Profile 3: Deep Intense Rock ---
    profile3 = {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False}
    recs3 = recommend_songs(profile3, songs, k=5)
    print("\n" + "=" * 50)
    print("  Deep Intense Rock Listener")
    print(f"  Genre: {profile3['genre']} | Mood: {profile3['mood']} | Energy: {profile3['energy']}")
    print("=" * 50)
    for i, rec in enumerate(recs3, start=1):
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 6.0")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        for reason in explanation.split(" | "):
            print(f"      + {reason}")
    print("\n" + "=" * 50)

    # --- Edge Case 1: High energy but sad mood (conflicting vibe) ---
    edge1 = {"genre": "r&b", "mood": "sad", "energy": 0.9, "likes_acoustic": False}
    recs_e1 = recommend_songs(edge1, songs, k=5)
    print("\n" + "=" * 50)
    print("  Edge Case: High Energy + Sad Mood")
    print(f"  Genre: {edge1['genre']} | Mood: {edge1['mood']} | Energy: {edge1['energy']}")
    print("=" * 50)
    for i, rec in enumerate(recs_e1, start=1):
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 6.0")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        for reason in explanation.split(" | "):
            print(f"      + {reason}")
    print("\n" + "=" * 50)

    # --- Edge Case 2: Low energy + angry mood (contradictory vibe) ---
    edge2 = {"genre": "metal", "mood": "angry", "energy": 0.1, "likes_acoustic": True}
    recs_e2 = recommend_songs(edge2, songs, k=5)
    print("\n" + "=" * 50)
    print("  Edge Case: Low Energy + Angry Mood")
    print(f"  Genre: {edge2['genre']} | Mood: {edge2['mood']} | Energy: {edge2['energy']}")
    print("=" * 50)
    for i, rec in enumerate(recs_e2, start=1):
        song, score, explanation = rec
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 6.0")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        for reason in explanation.split(" | "):
            print(f"      + {reason}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
