import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import json

def fetch_monthly_top100(year: int, month: int):
    base_url = "https://steamcharts.com/top/p.{}?month={}&year={}"
    all_games = []
    for page in [1, 2]:  # 1~100위 (1페이지 1~50, 2페이지 51~100)
        url = base_url.format(page, month, year)
        print(f"Fetching: {url}")
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", class_="common-table")
        if not table:
            print(f"No table found for {url}")
            continue
        for row in table.find_all("tr")[1:]:  # skip header
            cols = row.find_all("td")
            if len(cols) < 6:
                continue
            rank_str = cols[0].text.strip()
            rank = int(rank_str.replace('.', ''))
            game_link = cols[1].find("a")
            name = game_link.text.strip() if game_link else cols[1].text.strip()
            appid = None
            if game_link and "/app/" in game_link["href"]:
                m = re.search(r"/app/(\d+)", game_link["href"])
                if m:
                    appid = int(m.group(1))
            avg_players = int(cols[2].text.replace(",", "").strip())
            gain = cols[3].text.strip()
            peak_players = int(cols[4].text.replace(",", "").strip())
            all_games.append({
                "rank": rank,
                "appid": appid,
                "name": name,
                "avg_players": avg_players,
                "gain": gain,
                "peak_players": peak_players
            })
    return all_games

def save_monthly_top100(year: int, month: int, games: list):
    os.makedirs("data/raw", exist_ok=True)
    yyyymm = f"{year}{month:02d}"
    csv_path = f"data/raw/top100_games_{yyyymm}.csv"
    json_path = f"data/raw/top100_games_{yyyymm}.json"
    df = pd.DataFrame(games)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    print(f"Saved: {csv_path}, {json_path}")

def main():
    for year, month in [(2025, 3), (2025, 4), (2025, 5)]:
        try:
            games = fetch_monthly_top100(year, month)
            save_monthly_top100(year, month, games)
        except Exception as e:
            print(f"Error processing {year}-{month:02d}: {e}")

if __name__ == "__main__":
    main() 