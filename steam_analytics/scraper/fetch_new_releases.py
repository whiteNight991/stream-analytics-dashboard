import requests
import json
import os
from datetime import datetime, timedelta
import time
from pathlib import Path

class SteamNewReleasesFetcher:
    def __init__(self):
        self.base_url = "https://store.steampowered.com/api"
        self.raw_data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_new_releases(self, month="may_2025"):
        """
        Steam의 인기 출시 게임 데이터를 가져옵니다.
        
        Args:
            month (str): 월 정보 (예: "may_2025", "april_2025")
        """
        try:
            # 월 정보 파싱
            month_map = {
                "march_2025": (2025, 3),
                "april_2025": (2025, 4),
                "may_2025": (2025, 5)
            }
            
            if month not in month_map:
                print(f"❌ Invalid month: {month}")
                return None
                
            year, month_num = month_map[month]
            
            # 해당 월의 시작일과 종료일 계산
            start_date = datetime(year, month_num, 1)
            if month_num == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month_num + 1, 1) - timedelta(days=1)
            
            print(f"📅 Fetching new releases for {year}-{month_num:02d}")
            
            # Steam API를 통해 새로운 출시 게임 가져오기
            games_data = []
            page = 1
            
            while True:
                url = f"{self.base_url}/featuredcategories"
                params = {
                    "cc": "kr",
                    "l": "korean"
                }
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                new_releases = data.get('new_releases', {}).get('items', [])
                
                if not new_releases:
                    break
                
                for item in new_releases:
                    try:
                        # 출시일 파싱
                        release_date = datetime.fromtimestamp(item.get('release_date', {}).get('date', 0))
                        
                        # 해당 월의 게임만 필터링
                        if start_date <= release_date <= end_date:
                            game_data = {
                                "name": item.get('name', ''),
                                "appid": str(item.get('id', '')),
                                "release_date": release_date.strftime('%Y-%m-%d'),
                                "rating": item.get('review_score_desc', ''),
                                "tags": [tag.get('name', '') for tag in item.get('tags', [])[:5]]
                            }
                            games_data.append(game_data)
                            
                    except Exception as e:
                        print(f"⚠️ Error processing game: {e}")
                        continue
                
                page += 1
                time.sleep(1)  # API 요청 간 딜레이
            
            if games_data:
                # 파일 저장
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"new_releases_{month}_{timestamp}.json"
                filepath = self.raw_data_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(games_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ New releases data saved to: {filepath}")
                print(f"📊 Total games fetched: {len(games_data)}")
                
                return games_data
            else:
                print("❌ No game data found for the specified month")
                return None
                
        except requests.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def fetch_multiple_months(self, months=None):
        """
        여러 월의 데이터를 가져옵니다.
        
        Args:
            months (list): 월 목록 (예: ["march_2025", "april_2025", "may_2025"])
        """
        if months is None:
            months = ["march_2025", "april_2025", "may_2025"]
        
        all_data = {}
        for month in months:
            print(f"\n📅 Fetching data for {month}...")
            data = self.fetch_new_releases(month)
            if data:
                all_data[month] = data
            else:
                print(f"❌ Failed to fetch new releases data for {month}")
        
        return all_data

def main():
    print("\n🚀 Starting Steam New Releases data collection...\n")
    fetcher = SteamNewReleasesFetcher()
    fetcher.fetch_multiple_months()

if __name__ == "__main__":
    main() 