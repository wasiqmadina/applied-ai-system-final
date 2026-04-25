# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

My Model name: MoodMatch 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This is a classroom project, not something for real users. I built it to understand how content-based filtering works by actually coding it myself. It takes a user's preferred genre, mood, energy level, and whether they like acoustic or electronic sound, then finds the top 5 matching songs from a small catalog. It assumes the user knows what genre and mood they want upfront, which isn't always true in real life. It should not be used as an actual music app or to judge what music is good, it just matches labels.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song in the catalog gets a score based on how well it matches what the user said they want. There are four things it checks. First it checks if the mood matches, that's the biggest factor and worth the most points because getting the emotional feel wrong is the worst mistake. Then it checks how close the song's energy level is to what the user wants, so a song that's almost the same energy scores higher than one thats way off. Then it checks if the genre matches, which adds a smaller bonus. At the end it looks at whether the song is acoustic or electronic and rewards whichever the user prefers. All four scores get added up and the top 5 songs are returned. I changed the weights from the starter version so that mood and energy matter more than genre, because I think how a song makes you feel is more important than what label it falls under.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs. I started with 10 from the starter file and added 8 more to cover missing genres and moods. Genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, folk, r&b, metal, reggae, electronic, and country. Moods include happy, chill, intense, relaxed, focused, moody, uplifting, melancholic, nostalgic, sad, angry, peaceful, and romantic. Even with 18 songs it's still very small and most genres only have one song, so there isn't much variety within any category. There's also no world music or non-English genres and the mood labels are pretty simple compared to how complex emotions actually are when listening to music.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

It works best when the user's preferences are consistent and there are enough songs in the catalog that match. The chill lofi profile gave really good results — Library Rain and Midnight Coding were the clear top picks and they genuinely felt right for that kind of listener. The rock and pop profiles also made sense, with Storm Runner and Sunrise City ranking first. The scoring does a good job separating very different profiles from each other, a chill lofi user and a high-energy rock listener get completely different top 5 lists with no overlap, which is exactly what should happen. The explanation output is also a strength because every result comes with a breakdown showing exactly why it scored the way it did.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The biggest weakness I found during testing is that the mood matching is binary — either the song's mood exactly matches what the user wants, or it scores zero. This means a user looking for "chill" music gets no credit for "relaxed" or "peaceful" songs even though those feel basically the same in real life. When I ran the edge case profiles, songs that were clearly a good fit emotionally got completely ignored just because their mood label was slightly different. This also means users whose preferred mood doesn't appear in the catalog at all silently get the worst possible recommendations, the system doesn't warn them, it just ranks everything by energy instead. A related issue is that lofi has 3 songs in the catalog while most other genres only have 1, so lofi users get more meaningful genre-based differentiation while someone who likes country or reggae only ever sees that genre bonus apply to a single song, which makes their results feel more random and less personalized.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested five different user profiles to see how the system behaved across different situations. The first was a chill lofi listener (genre: lofi, mood: chill, energy: 0.38) which was the main profile the system was built around. The second was a high-energy pop fan (genre: pop, mood: happy, energy: 0.85) to see if the system could handle a completely different vibe. The third was a deep intense rock listener (genre: rock, mood: intense, energy: 0.92) to test the high-energy end of the spectrum. Then I ran two edge cases on purpose, one with a conflicting profile (genre: r&b, mood: sad, energy: 0.9, which is basically asking for angry sad music at full volume) and one with a contradictory vibe (genre: metal, mood: angry, energy: 0.1, which is asking for calm angry music).

The normal profiles mostly gave results that made sense. Library Rain came up first for the chill lofi user, Storm Runner first for the rock listener, and Sunrise City first for the pop fan. Those felt right when I looked at the song attributes.

What surprised me was the edge cases. For the high energy + sad mood profile, the system still picked 3AM Feelings as the top result even after I doubled the energy weight. That song has an energy of 0.51 but the user wanted 0.9 which is a huge gap but it still won because it was the only sad song in the catalog. The system basically had no choice. It showed me that the algorithm can only work with what's in the dataset, and if a mood only has one song representing it, that song will always win for that mood no matter how wrong the energy is.

The other surprise was the low energy + angry profile. After changing the weights to prioritize energy more, Shatter the Wall (the metal song with 0.97 energy) actually dropped to third place, and calm classical and ambient songs ranked above it just because they were closer in energy to 0.1. That was interesting because those songs have nothing to do with the angry mood — but the system rewarded them anyway because energy became the dominant signal.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

The first thing I would change is making mood matching less strict. Similar moods like chill, relaxed, and peaceful should get partial credit instead of zero, so the system stops ignoring songs that are clearly in the right emotional neighborhood. Second I would add a rule so the same artist can't appear twice in the top 5, right now LoRoom shows up at both #1 and #4 for the chill profile which feels repetitive. Third I would expand the catalog, even just to 100 songs with more balanced genre and mood distribution, because when a mood only has one song in the catalog that song always wins regardless of how bad the energy match is.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

For this version I used Claude Code as an AI assistant to help add the Groq explanation layer, the output guardrail, and the test harness on top of the original scoring system. Something that was actually helpful was when it suggested the guardrail with a fallback instead of just crashing if the API fails — I wouldn't have thought to do that. Something that went wrong was it gave me a model name (`llama3-8b-8192`) that was already decommissioned by Groq, so the entire first test run failed. I had to look up the correct model name myself and swap it out. It was a good reminder that you still have to verify what an AI tells you, especially about external services.

Building this made me realize how much goes into something that feels automatic when you use Spotify. The hardest part wasn't writing the code, it was deciding what the weights should be and realizing every choice had tradeoffs. Making mood worth more than genre felt right to me but that one decision meant a song with the wrong mood label would always lose no matter how good its energy or acousticness was. The most unexpected thing was finding out that the edge cases exposed catalog problems more than algorithm problems. When the sad plus high-energy profile kept returning a slow song my first instinct was that the weights were wrong, but the real issue was there was only one sad song in the whole catalog. That made me think Spotify's recommendation quality probably depends just as much on having a huge diverse library as on its algorithm, a perfect formula with bad data still gives bad results.  
