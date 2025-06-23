import json
import os
from collections import Counter
import matplotlib.pyplot as plt

def load_latest_metadata():
    raw_data_dir = "data/raw"
    files = [f for f in os.listdir(raw_data_dir) if f.startswith("game_metadata_")]
    if not files:
        raise FileNotFoundError("No game metadata file found.")
    latest_file = max(files)
    with open(os.path.join(raw_data_dir, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_genres(metadata):
    genres = []
    categories = []
    for game in metadata.values():
        genres.extend(game.get("genres", []))
        categories.extend(game.get("categories", []))
    genre_counts = Counter(genres)
    category_counts = Counter(categories)
    return genre_counts, category_counts

def plot_top_genres(genre_counts, top_n=10):
    top = genre_counts.most_common(top_n)
    labels, values = zip(*top)
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(f"Top {top_n} Game Genres")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/raw/top_genres.png")
    plt.close()

def plot_top_categories(category_counts, top_n=10):
    top = category_counts.most_common(top_n)
    labels, values = zip(*top)
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(f"Top {top_n} Game Categories")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/raw/top_categories.png")
    plt.close()

def main():
    metadata = load_latest_metadata()
    genre_counts, category_counts = analyze_genres(metadata)
    print("Top Genres:")
    for genre, count in genre_counts.most_common(10):
        print(f"{genre}: {count}")
    print("\nTop Categories:")
    for cat, count in category_counts.most_common(10):
        print(f"{cat}: {count}")
    plot_top_genres(genre_counts)
    plot_top_categories(category_counts)
    print("Saved bar charts to data/raw/")

if __name__ == "__main__":
    main() 