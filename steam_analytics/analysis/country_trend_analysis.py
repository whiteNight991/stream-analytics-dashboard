import json
import os
import pandas as pd
from collections import Counter
from typing import Dict, List, Tuple

def load_latest_country_stats():
    """Load the most recent country statistics file"""
    raw_data_dir = "data/raw/country_stats"
    files = [f for f in os.listdir(raw_data_dir) if f.startswith("country_stats_")]
    if not files:
        raise FileNotFoundError("No country statistics file found.")
    latest_file = max(files)
    with open(os.path.join(raw_data_dir, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_country_trends(stats: Dict) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Analyze trends across countries"""
    # 1. 국가별 인기 게임 분석
    country_top_games = {}
    for country, data in stats.items():
        top_games = [game["name"] for game in data["top_sellers"]]
        country_top_games[country] = top_games
    
    # 2. 국가별 가격 분석
    country_prices = {}
    for country, data in stats.items():
        prices = [game["price"] for game in data["top_sellers"]]
        country_prices[country] = {
            "avg_price": sum(prices) / len(prices) if prices else 0,
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0
        }
    
    # 3. 국가별 할인율 분석
    country_discounts = {}
    for country, data in stats.items():
        discounts = [game["discount"] for game in data["specials"]]
        country_discounts[country] = {
            "avg_discount": sum(discounts) / len(discounts) if discounts else 0,
            "max_discount": max(discounts) if discounts else 0
        }
    
    # 데이터프레임 생성
    price_df = pd.DataFrame.from_dict(country_prices, orient='index')
    discount_df = pd.DataFrame.from_dict(country_discounts, orient='index')
    
    # 게임 인기도 데이터프레임 생성
    game_popularity = {}
    for country, games in country_top_games.items():
        for game in games:
            if game not in game_popularity:
                game_popularity[game] = {}
            game_popularity[game][country] = game_popularity[game].get(country, 0) + 1
    
    popularity_df = pd.DataFrame.from_dict(game_popularity, orient='index')
    popularity_df = popularity_df.fillna(0)
    
    return price_df, discount_df, popularity_df

def main():
    stats = load_latest_country_stats()
    price_df, discount_df, popularity_df = analyze_country_trends(stats)
    
    print("\n=== 국가별 평균 가격 분석 ===")
    print(price_df.sort_values('avg_price', ascending=False))
    
    print("\n=== 국가별 할인율 분석 ===")
    print(discount_df.sort_values('avg_discount', ascending=False))
    
    print("\n=== 게임별 국가 인기도 분석 ===")
    # 상위 10개 게임만 표시
    top_games = popularity_df.sum(axis=1).sort_values(ascending=False).head(10)
    print(top_games)

if __name__ == "__main__":
    main() 