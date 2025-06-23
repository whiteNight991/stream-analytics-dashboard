import json
import os
import pandas as pd
import matplotlib.pyplot as plt

def load_latest_top100():
    raw_data_dir = "data/raw"
    files = [f for f in os.listdir(raw_data_dir) if f.startswith("top100_games_")]
    if not files:
        raise FileNotFoundError("No top100 games file found.")
    latest_file = max(files)
    with open(os.path.join(raw_data_dir, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def load_latest_metadata():
    raw_data_dir = "data/raw"
    files = [f for f in os.listdir(raw_data_dir) if f.startswith("game_metadata_")]
    if not files:
        raise FileNotFoundError("No game metadata file found.")
    latest_file = max(files)
    with open(os.path.join(raw_data_dir, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    top100 = load_latest_top100()
    metadata = load_latest_metadata()
    # 상위 10개 게임 추출
    top10 = sorted(top100, key=lambda x: x["current_players"], reverse=True)[:10]
    rows = []
    for game in top10:
        appid = game["appid"]
        meta = metadata.get(str(appid)) or metadata.get(appid) or {}
        rows.append({
            "Rank": game["rank"],
            "Name": meta.get("name", appid),
            "Current Players": game["current_players"],
            "Peak": game["peak_in_game"],
            "Genres": ", ".join(meta.get("genres", [])),
            "Release": meta.get("release_date", "")
        })
    df = pd.DataFrame(rows)
    print(df)
    # Bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(df["Name"], df["Current Players"])
    plt.title("Top 10 Games by Current Players")
    plt.ylabel("Current Players")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data/raw/top10_games.png")
    plt.close()
    print("Saved bar chart to data/raw/top10_games.png")

if __name__ == "__main__":
    main() 