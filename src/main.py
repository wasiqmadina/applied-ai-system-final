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
        print(f"    Score : {score:.2f} / 5.0")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"      + {reason}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
