import json

# Load top 100 games data
with open('data/raw/top100_games_20250617_093209.json', 'r') as f:
    top100 = json.load(f)

# Get 8th, 9th, 10th top games by current players
top10 = sorted(top100, key=lambda x: x["current_players"], reverse=True)[:10]
for i in range(7, 10):
    game = top10[i]
    print(f"Rank {i+1}: appid={game['appid']}, current_players={game['current_players']}")

# Load metadata
with open('data/raw/game_metadata_093209.json', 'r', encoding='utf-8') as f:
    metadata = json.load(f)

for i in range(7, 10):
    game = top10[i]
    appid = str(game['appid'])
    meta = metadata.get(appid)
    print(f"\n[Metadata for appid {appid}]")
    if meta:
        print(f"  Name: {meta.get('name')}")
        print(f"  Genres: {meta.get('genres')}")
        print(f"  Release: {meta.get('release_date')}")
    else:
        print("  No metadata found.") 