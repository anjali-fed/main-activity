import time
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore

init(autoreset=True)

# Manually entered movie data
movies = [
    {
        "Series_Title": "The Shawshank Redemption",
        "Genre": "Drama",
        "Overview": "Two imprisoned men bond over years and find hope through friendship.",
        "IMDB_Rating": 9.3
    },
    {
        "Series_Title": "The Dark Knight",
        "Genre": "Action, Crime, Drama",
        "Overview": "Batman faces the Joker, a criminal mastermind causing chaos in Gotham.",
        "IMDB_Rating": 9.0
    },
    {
        "Series_Title": "Inception",
        "Genre": "Action, Adventure, Sci-Fi",
        "Overview": "A thief enters people's dreams to steal secrets and plant ideas.",
        "IMDB_Rating": 8.8
    },
    {
        "Series_Title": "Forrest Gump",
        "Genre": "Drama, Romance",
        "Overview": "A kind-hearted man experiences extraordinary events throughout his life.",
        "IMDB_Rating": 8.8
    },
    {
        "Series_Title": "Interstellar",
        "Genre": "Adventure, Drama, Sci-Fi",
        "Overview": "A team of explorers travels through a wormhole in space to save humanity.",
        "IMDB_Rating": 8.7
    },
    {
        "Series_Title": "Toy Story",
        "Genre": "Animation, Adventure, Comedy",
        "Overview": "Toys come to life and embark on exciting adventures.",
        "IMDB_Rating": 8.3
    },
    {
        "Series_Title": "Finding Nemo",
        "Genre": "Animation, Adventure, Comedy",
        "Overview": "A clownfish searches the ocean to find his lost son.",
        "IMDB_Rating": 8.2
    },
    {
        "Series_Title": "The Lion King",
        "Genre": "Animation, Adventure, Drama",
        "Overview": "A young lion prince learns responsibility and courage.",
        "IMDB_Rating": 8.5
    }
]

df = pd.DataFrame(movies)

genres = sorted(
    {
        g.strip()
        for xs in df["Genre"].dropna().str.split(", ")
        for g in xs
    }
)

def dots():
    for _ in range(3):
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)

def senti(p):
    return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"

def recommend(genre=None, mood=None, rating=None, n=5):
    d = df

    if genre:
        d = d[d["Genre"].str.contains(genre, case=False, na=False)]

    if rating is not None:
        d = d[d["IMDB_Rating"] >= rating]

    if d.empty:
        return "No suitable movie recommendations found."

    d = d.sample(frac=1).reset_index(drop=True)

    need_nonneg = bool(mood)
    out = []

    for _, r in d.iterrows():
        ov = r.get("Overview")

        if pd.isna(ov):
            continue

        pol = TextBlob(ov).sentiment.polarity

        if (not need_nonneg) or pol >= 0:
            out.append((r["Series_Title"], pol))

            if len(out) == n:
                break

    return out if out else "No suitable movie recommendations found."

def show(recs, name):
    print(Fore.YELLOW + f"\n🍿 AI-Analyzed Movie Recommendations for {name}:")

    for i, (t, p) in enumerate(recs, 1):
        print(
            f"{Fore.CYAN}{i}. 🎥 {t} "
            f"(Polarity: {p:.2f}, {senti(p)})"
        )

def get_genre():
    print(Fore.GREEN + "Available Genres:\n")

    for i, g in enumerate(genres, 1):
        print(f"{Fore.CYAN}{i}. {g}")

    print()

    while True:
        x = input(
            Fore.YELLOW + "Enter genre number or name: "
        ).strip()

        if x.isdigit() and 1 <= int(x) <= len(genres):
            return genres[int(x) - 1]

        x = x.title()

        if x in genres:
            return x

        print(Fore.RED + "Invalid input. Try again.\n")

def get_rating():
    while True:
        x = input(
            Fore.YELLOW +
            "Enter minimum IMDB rating (8.0-9.3) or 'skip': "
        ).strip()

        if x.lower() == "skip":
            return None

        try:
            r = float(x)

            if 8.0 <= r <= 9.3:
                return r

            print(Fore.RED + "Rating out of range. Try again.\n")

        except ValueError:
            print(Fore.RED + "Invalid input. Try again.\n")

print(
    Fore.BLUE +
    "🎥 Welcome to your Personal Movie Recommendation Assistant! 🎥\n"
)

name = input(Fore.YELLOW + "What's your name? ").strip()

print(f"\n{Fore.GREEN}Great to meet you, {name}!\n")

print(
    Fore.BLUE +
    "\n🔍 Let's find the perfect movie for you!\n"
)

genre = get_genre()

mood = input(
    Fore.YELLOW +
    "How do you feel today? (Describe your mood): "
).strip()

print(
    Fore.BLUE +
    "\nAnalyzing mood",
    end="",
    flush=True
)

dots()

mp = TextBlob(mood).sentiment.polarity

md = (
    "positive 😊"
    if mp > 0
    else "negative 😞"
    if mp < 0
    else "neutral 😐"
)

print(
    f"\n{Fore.GREEN}Your mood is {md} "
    f"(Polarity: {mp:.2f}).\n"
)

rating = get_rating()

print(
    f"{Fore.BLUE}\nFinding movies for {name}",
    end="",
    flush=True
)

dots()

recs = recommend(
    genre=genre,
    mood=mood,
    rating=rating,
    n=5
)

if isinstance(recs, str):
    print(Fore.RED + recs + "\n")
else:
    show(recs, name)

while True:
    a = input(
        Fore.YELLOW +
        "\nWould you like more recommendations? (yes/no): "
    ).strip().lower()

    if a == "no":
        print(
            Fore.GREEN +
            f"\nEnjoy your movie picks, {name}! 🎬🍿\n"
        )
        break

    elif a == "yes":
        recs = recommend(
            genre=genre,
            mood=mood,
            rating=rating,
            n=5
        )

        if isinstance(recs, str):
            print(Fore.RED + recs + "\n")
        else:
            show(recs, name)

    else:
        print(Fore.RED + "Invalid choice. Try again.\n")