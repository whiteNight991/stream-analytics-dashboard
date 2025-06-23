import requests
import json
from datetime import datetime
import os
from typing import Dict, List, Optional
from config import STEAM_API_KEY
import pandas as pd

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

    def save_to_csv(self, data: List[Dict], filename: str):
        """Save data to a CSV file"""
        os.makedirs("data/raw", exist_ok=True)
        filepath = os.path.join("data/raw", filename)
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding="utf-8")

def main():
    fetcher = SteamDataFetcher(STEAM_API_KEY)
    
    # 현재 시간을 파일명에 포함
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Top 100 게임 데이터 수집
    print("Fetching top 100 games...")
    top_games = fetcher.get_top_100_games()
    
    if not top_games:
        print("Failed to fetch top 100 games. Please check your API key and try again.")
        return
    
    print(f"Successfully fetched {len(top_games)} games")
    
    # 각 게임의 상세 정보 수집
    print("Fetching current player counts...")
    for i, game in enumerate(top_games, 1):
        player_count = fetcher.get_current_players(game["appid"])
        game["current_players"] = player_count if player_count is not None else 0
        print(f"Progress: {i}/100 games processed")
    
    # 데이터 저장
    json_filename = f"top100_games_{timestamp}.json"
    fetcher.save_to_json(top_games, json_filename)
    print(f"Successfully saved top 100 games data to data/raw/{json_filename}")

    csv_filename = f"top100_games_{timestamp}.csv"
    fetcher.save_to_csv(top_games, csv_filename)
    print(f"Successfully saved top 100 games data to data/raw/{csv_filename}")

if __name__ == "__main__":
    main()
