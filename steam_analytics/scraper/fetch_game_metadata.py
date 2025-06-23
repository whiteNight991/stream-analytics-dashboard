from pdb import main
import requests
import json
from datetime import datetime
import os
from typing import List, Dict, Optional
from config import STEAM_API_KEY

class SteamDataFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.steampowered.com"

    def get_current_players(self, app_id: int) -> Optional[int]:
        """Get current number of players for a specific game"""
        url = f"{self.base_url}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
        params = {
            "appid": app_id,
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data["response"]["player_count"]
        except Exception as e:
            print(f"Error fetching player count for app_id {app_id}: {str(e)}")
            return None

    def get_top_100_games(self) -> List[Dict]:
        """Get top 100 games by current player count"""
        url = f"{self.base_url}/ISteamChartsService/GetMostPlayedGames/v1/"
        params = {
            "key": self.api_key,
            "limit": 100
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data["response"]["ranks"]
        except Exception as e:
            print(f"Error fetching top 100 games: {str(e)}")
            return []

    def save_to_json(self, data: List[Dict], filename: str):
        """Save data to a JSON file"""
        os.makedirs("data/raw", exist_ok=True)
        filepath = os.path.join("data/raw", filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class SteamGameMetadata:
    def __init__(self):
        self.base_url = "https://store.steampowered.com/api/appdetails"
        
    def get_game_details(self, app_id: int) -> Optional[Dict]:
        """Get detailed information about a game from the Steam store API"""
        params = {
            "appids": app_id
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if str(app_id) in data and data[str(app_id)]["success"]:
                return data[str(app_id)]["data"]
            return None
        except Exception as e:
            print(f"Error fetching game details for app_id {app_id}: {str(e)}")
            return None

    def save_to_json(self, data: Dict, filename: str):
        """Save data to a JSON file"""
        os.makedirs("data/raw", exist_ok=True)
        filepath = os.path.join("data/raw", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 이전에 수집한 top 100 게임 데이터 읽기
    raw_data_dir = "data/raw"
    top_games_files = [f for f in os.listdir(raw_data_dir) if f.startswith("top100_games_")]
    if not top_games_files:
        print("No top 100 games data found. Please run fetch_realtime_top100.py first.")
        return
    latest_file = max(top_games_files)
    with open(os.path.join(raw_data_dir, latest_file), "r", encoding="utf-8") as f:
        top_games = json.load(f)
    # 게임 메타데이터 수집
    metadata_fetcher = SteamGameMetadata()
    game_metadata = {}
    print("Fetching game metadata...")
    for i, game in enumerate(top_games, 1):
        app_id = game["appid"]
        print(f"Progress: {i}/100 games processed")
        details = metadata_fetcher.get_game_details(app_id)
        if details:
            game_metadata[app_id] = {
                "name": details.get("name", "Unknown"),
                "genres": [genre["description"] for genre in details.get("genres", [])],
                "release_date": details.get("release_date", {}).get("date", "Unknown"),
                "price": details.get("price_overview", {}).get("final", 0) / 100 if details.get("price_overview") else 0,
                "categories": [cat["description"] for cat in details.get("categories", [])],
                "short_description": details.get("short_description", ""),
                "header_image": details.get("header_image", "")
            }
    # 메타데이터 저장
    timestamp = latest_file.split("_")[-1].split(".")[0]
    metadata_fetcher.save_to_json(game_metadata, f"game_metadata_{timestamp}.json")
    print(f"Successfully saved game metadata to data/raw/game_metadata_{timestamp}.json")

if __name__ == "__main__":
    main()