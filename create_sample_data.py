#!/usr/bin/env python3
"""
샘플 데이터 생성 스크립트
Streamlit Cloud 배포를 위한 샘플 데이터를 생성합니다.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def create_sample_top100_data():
    """샘플 Top 100 게임 데이터 생성"""
    sample_data = [
        {
            "rank": 1,
            "appid": 730,
            "current_players": 850000,
            "peak_in_game": 1200000,
            "name": "Counter-Strike 2"
        },
        {
            "rank": 2,
            "appid": 570,
            "current_players": 650000,
            "peak_in_game": 800000,
            "name": "Dota 2"
        },
        {
            "rank": 3,
            "appid": 1172470,
            "current_players": 450000,
            "peak_in_game": 600000,
            "name": "Apex Legends"
        },
        {
            "rank": 4,
            "appid": 252490,
            "current_players": 400000,
            "peak_in_game": 550000,
            "name": "Rust"
        },
        {
            "rank": 5,
            "appid": 271590,
            "current_players": 350000,
            "peak_in_game": 500000,
            "name": "Grand Theft Auto V"
        },
        {
            "rank": 6,
            "appid": 578080,
            "current_players": 300000,
            "peak_in_game": 450000,
            "name": "PUBG: BATTLEGROUNDS"
        },
        {
            "rank": 7,
            "appid": 1091500,
            "current_players": 280000,
            "peak_in_game": 400000,
            "name": "Cyberpunk 2077"
        },
        {
            "rank": 8,
            "appid": 1245620,
            "current_players": 250000,
            "peak_in_game": 350000,
            "name": "Elden Ring"
        },
        {
            "rank": 9,
            "appid": 1222670,
            "current_players": 220000,
            "peak_in_game": 320000,
            "name": "The Witcher 3: Wild Hunt"
        },
        {
            "rank": 10,
            "appid": 1144200,
            "current_players": 200000,
            "peak_in_game": 300000,
            "name": "Red Dead Redemption 2"
        }
    ]
    
    # 데이터 디렉토리 생성
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"top100_games_{timestamp}.json"
    filepath = data_dir / filename
    
    # JSON 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 샘플 Top 100 데이터 생성됨: {filepath}")
    return filename

def create_sample_metadata():
    """샘플 게임 메타데이터 생성"""
    sample_metadata = {
        "730": {
            "name": "Counter-Strike 2",
            "genres": ["Action", "FPS", "Shooter"],
            "categories": ["Multi-player", "Online PvP", "Valve Anti-Cheat enabled"],
            "release_date": "2023-09-27",
            "price": 0.0,
            "short_description": "Counter-Strike 2 is the largest technical leap forward in Counter-Strike history.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg"
        },
        "570": {
            "name": "Dota 2",
            "genres": ["Action", "Strategy", "MOBA"],
            "categories": ["Multi-player", "Online PvP", "Valve Anti-Cheat enabled"],
            "release_date": "2013-07-09",
            "price": 0.0,
            "short_description": "Every day, millions of players worldwide enter battle as one of over a hundred Dota heroes.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/570/header.jpg"
        },
        "1172470": {
            "name": "Apex Legends",
            "genres": ["Action", "Adventure", "FPS"],
            "categories": ["Multi-player", "Online PvP", "Battle Royale"],
            "release_date": "2020-11-05",
            "price": 0.0,
            "short_description": "Apex Legends is the award-winning, free-to-play Hero shooter from Respawn Entertainment.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/1172470/header.jpg"
        },
        "252490": {
            "name": "Rust",
            "genres": ["Action", "Adventure", "Survival"],
            "categories": ["Multi-player", "Online PvP", "Survival"],
            "release_date": "2018-02-08",
            "price": 39.99,
            "short_description": "The only aim in Rust is to survive. Everything wants you to die - the island's wildlife and other inhabitants.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/252490/header.jpg"
        },
        "271590": {
            "name": "Grand Theft Auto V",
            "genres": ["Action", "Adventure"],
            "categories": ["Multi-player", "Online PvP", "Single-player"],
            "release_date": "2015-04-14",
            "price": 29.99,
            "short_description": "Grand Theft Auto V for PC offers players the option to explore the award-winning world of Los Santos.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/271590/header.jpg"
        },
        "578080": {
            "name": "PUBG: BATTLEGROUNDS",
            "genres": ["Action", "Adventure", "Battle Royale"],
            "categories": ["Multi-player", "Online PvP", "Battle Royale"],
            "release_date": "2017-12-21",
            "price": 0.0,
            "short_description": "PUBG: BATTLEGROUNDS is a battle royale shooter that pits 100 players against each other.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/578080/header.jpg"
        },
        "1091500": {
            "name": "Cyberpunk 2077",
            "genres": ["RPG", "Action", "Adventure"],
            "categories": ["Single-player", "RPG", "Story Rich"],
            "release_date": "2020-12-10",
            "price": 59.99,
            "short_description": "Cyberpunk 2077 is an open-world, action-adventure story set in Night City.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg"
        },
        "1245620": {
            "name": "Elden Ring",
            "genres": ["Action", "RPG"],
            "categories": ["Single-player", "RPG", "Souls-like"],
            "release_date": "2022-02-25",
            "price": 59.99,
            "short_description": "THE NEW FANTASY ACTION RPG. Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg"
        },
        "1222670": {
            "name": "The Witcher 3: Wild Hunt",
            "genres": ["RPG", "Action", "Adventure"],
            "categories": ["Single-player", "RPG", "Story Rich"],
            "release_date": "2015-05-19",
            "price": 39.99,
            "short_description": "You are Geralt of Rivia, mercenary monster slayer. Before you stands a war-torn, monster-infested continent.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/1222670/header.jpg"
        },
        "1144200": {
            "name": "Red Dead Redemption 2",
            "genres": ["Action", "Adventure"],
            "categories": ["Single-player", "Multi-player", "Story Rich"],
            "release_date": "2019-12-05",
            "price": 59.99,
            "short_description": "Red Dead Redemption 2 is the epic tale of Arthur Morgan and the Van der Linde gang.",
            "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/1144200/header.jpg"
        }
    }
    
    # 데이터 디렉토리 생성
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"game_metadata_{timestamp}.json"
    filepath = data_dir / filename
    
    # JSON 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sample_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 샘플 메타데이터 생성됨: {filepath}")
    return filename

def main():
    """메인 함수"""
    print("🎮 Steam Analytics 샘플 데이터 생성 중...")
    print("=" * 50)
    
    # 샘플 데이터 생성
    top100_file = create_sample_top100_data()
    metadata_file = create_sample_metadata()
    
    print("=" * 50)
    print("✅ 모든 샘플 데이터 생성 완료!")
    print(f"📊 Top 100 데이터: {top100_file}")
    print(f"📋 메타데이터: {metadata_file}")
    print("\n🚀 이제 Streamlit Cloud에서 배포할 수 있습니다!")

if __name__ == "__main__":
    main() 