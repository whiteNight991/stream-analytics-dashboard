import streamlit as st
import pandas as pd
import json
import os
from PIL import Image
import sys
from pathlib import Path
from datetime import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Add scraper directory to Python path for importing config and scraper modules
scraper_path = str(Path(__file__).parent.parent / "scraper")
if scraper_path not in sys.path:
    sys.path.append(scraper_path)

# --- DEBUGGING PRINTS ---
print(f"DEBUG: Project Root Path added to sys.path: {project_root}")
print(f"DEBUG: Scraper Path added to sys.path: {scraper_path}")
print(f"DEBUG: Current sys.path: {sys.path}")
# --- END DEBUGGING PRINTS ---

# Modified imports to use absolute path from steam_analytics package
from steam_analytics.scraper.config import STEAM_API_KEY
from steam_analytics.scraper.fetch_realtime_top100 import SteamDataFetcher
from steam_analytics.scraper.fetch_game_metadata import SteamGameMetadata

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
# Windows에서 한글 폰트 설정
if os.name == 'nt':  # Windows
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux/Mac
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
# 음수 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

@st.cache_data(ttl=3600) # Cache data for 1 hour
def load_latest_top100():
    raw_data_dir = os.path.join(str(Path(__file__).parent.parent.parent), "data", "raw")
    files = [f for f in os.listdir(raw_data_dir) if f.startswith("top100_games_") and f.endswith(".json")]
    if not files:
        st.error("No top100 games JSON file found. Please refresh data.")
        return None
    latest_file = max(files)
    filepath = os.path.join(raw_data_dir, latest_file)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure 'current_players' is an integer, default to 0 if missing or invalid
        for game in data:
            game['current_players'] = int(game.get('current_players', 0))
        return data
    except Exception as e:
        st.error(f"Error loading top100 games JSON: {e}")
        return None

@st.cache_data(ttl=3600) # Cache data for 1 hour
def load_latest_metadata():
    raw_data_dir = os.path.join(str(Path(__file__).parent.parent.parent), "data", "raw")
    files = [f for f in os.listdir(raw_data_dir) if f.startswith("game_metadata_")]
    if not files:
        st.error("No game metadata file found. Please refresh data.")
        return None
    latest_file = max(files)
    with open(os.path.join(raw_data_dir, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    return None

def main():
    load_css("static/style.css")
    
    # 메인 타이틀
    st.title("스팀 Application 분석")

    # 사이드바에서 시각화 선택
    st.sidebar.title("카테고리")
    visualization = st.sidebar.selectbox(
        "원하는 분석을 선택하세요:",
        [
            "Top 10 동시접속자수",
            "인기 장르 분석",
            "인기 카테고리 분석", 
            "게임 세부 검색"
        ]
    )
    
    top100 = load_latest_top100() # 이제 CSV에서 읽어옴 -> JSON에서 읽어오도록 수정
    metadata = load_latest_metadata()

    if top100 is None or metadata is None:
        st.info("데이터가 로드되지 않았습니다. 스크레이퍼를 수동으로 실행해주세요.")
        return

    if visualization == "Top 10 동시접속자수":
        st.header("Top 10 동시접속자수") 
        # 메타데이터가 있는 게임만 추출
        # current_players 키가 없을 경우 0으로 처리하여 KeyError 방지
        filtered = [g for g in sorted(top100, key=lambda x: x.get("current_players", 0), reverse=True) if (str(g["appid"]) in metadata or g["appid"] in metadata)]
        top10 = filtered[:10]
        st.write(f"총 {len(filtered)}개 게임 중 메타데이터가 있는 상위 10개만 표시")
        rows = []
        for i, game in enumerate(top10):
            appid = game["appid"]
            meta = metadata.get(str(appid)) or metadata.get(appid) or {}
            rows.append({
                "Rank": game["rank"],
                "Name": meta.get("name", f"Unknown ({appid})"),
                "Current Players": game.get("current_players", 0),
                "Peak": game.get("peak_in_game", 0),
                "Genres": ", ".join(meta.get("genres", [])),
                "Release": meta.get("release_date", "")
            })
        df = pd.DataFrame(rows).reset_index(drop=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 차트 데이터 검증
        chart_data = df["Current Players"].copy()
        chart_data = pd.to_numeric(chart_data, errors='coerce').fillna(0)
        chart_data = chart_data.clip(lower=0)
        
        if chart_data.max() > 0:
            if df['Name'].is_unique:
                chart_df = df.set_index("Name")["Current Players"]
                chart_df = pd.to_numeric(chart_df, errors='coerce').fillna(0).clip(lower=0)
                st.bar_chart(chart_df)
            else:
                st.bar_chart(chart_data)
        else:
            st.info("차트를 표시할 수 있는 유효한 데이터가 없습니다.")

    elif visualization == "인기 장르 분석":
        st.header("인기 장르 분석") 
        
        # 장르별 현재 접속자수 계산
        genre_players = {}
        genre_game_counts = {}
        
        for game in top100:
            appid = game["appid"]
            current_players = game.get("current_players", 0)
            
            # 메타데이터에서 장르 정보 가져오기
            meta = metadata.get(str(appid)) or metadata.get(appid) or {}
            genres = meta.get("genres", [])
            
            # 각 장르에 현재 접속자수 추가
            for genre in genres:
                if genre not in genre_players:
                    genre_players[genre] = 0
                    genre_game_counts[genre] = 0
                genre_players[genre] += current_players
                genre_game_counts[genre] += 1
        
        # 상위 10개 장르 선택 (접속자수 기준)
        top_genres_by_players = sorted(genre_players.items(), key=lambda x: x[1], reverse=True)[:10]
        top_genres_by_games = sorted(genre_game_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 두 개의 컬럼으로 나누어 표시
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("장르별 현재 접속자수")
            if top_genres_by_players:
                genre_players_df = pd.DataFrame(top_genres_by_players, columns=['Genre', 'Current Players'])
                st.bar_chart(genre_players_df.set_index('Genre'))
                st.dataframe(genre_players_df, use_container_width=True, hide_index=True)
            else:
                st.info("장르별 접속자수 데이터가 없습니다.")
        
        with col2:
            st.subheader("장르별 게임 수")
            if top_genres_by_games:
                genre_games_df = pd.DataFrame(top_genres_by_games, columns=['Genre', 'Game Count'])
                st.bar_chart(genre_games_df.set_index('Genre'))
                st.dataframe(genre_games_df, use_container_width=True, hide_index=True)
            else:
                st.info("장르별 게임 수 데이터가 없습니다.")
        
        # 상세 통계
        st.subheader("장르별 상세 통계")
        
        # 통계 유형 선택
        stat_type = st.selectbox(
            "통계 유형 선택:",
            ["접속자수 기준", "게임 수 기준", "평균 접속자수 기준"],
            index=0
        )
        
        detailed_stats = []
        for genre in set(genre_players.keys()) | set(genre_game_counts.keys()):
            players = genre_players.get(genre, 0)
            games = genre_game_counts.get(genre, 0)
            avg_players = players / games if games > 0 else 0
            detailed_stats.append({
                'Genre': genre,
                'Total Players': players,
                'Game Count': games,
                'Avg Players per Game': round(avg_players, 1)
            })
        
        detailed_df = pd.DataFrame(detailed_stats)
        
        # 선택된 통계 유형에 따라 정렬
        if stat_type == "접속자수 기준":
            detailed_df = detailed_df.sort_values('Total Players', ascending=False)
            chart_data = detailed_df[['Genre', 'Total Players']].head(10)
            chart_column = 'Total Players'
            title = "장르별 접속자수 분포 (상위 10개)"
        elif stat_type == "게임 수 기준":
            detailed_df = detailed_df.sort_values('Game Count', ascending=False)
            chart_data = detailed_df[['Genre', 'Game Count']].head(10)
            chart_column = 'Game Count'
            title = "장르별 게임 수 분포 (상위 10개)"
        else:  # 평균 접속자수 기준
            detailed_df = detailed_df.sort_values('Avg Players per Game', ascending=False)
            chart_data = detailed_df[['Genre', 'Avg Players per Game']].head(10)
            chart_column = 'Avg Players per Game'
            title = "장르별 평균 접속자수 분포 (상위 10개)"
        
        # 원형 차트 생성
        if not chart_data.empty:
            # 퍼센티지 계산
            total_value = chart_data[chart_column].sum()
            chart_data['Percentage'] = (chart_data[chart_column] / total_value * 100).round(1)
            
            # 원형 차트 표시
            st.subheader(f"📊 {title}")
            
            # 두 개의 컬럼으로 나누어 표시
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # 원형 차트 (matplotlib 사용)
                fig, ax = plt.subplots(figsize=(10, 8))
                
                # 한글 폰트 명시적 설정
                if os.name == 'nt':  # Windows
                    plt.rcParams['font.family'] = 'Malgun Gothic'
                else:  # Linux/Mac
                    plt.rcParams['font.family'] = 'DejaVu Sans'
                plt.rcParams['axes.unicode_minus'] = False
                
                wedges, texts, autotexts = ax.pie(
                    chart_data[chart_column], 
                    labels=chart_data['Genre'],
                    autopct='%1.1f%%',
                    startangle=90
                )
                
                # 텍스트 스타일 개선
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                
                # 라벨 텍스트 스타일 개선
                for text in texts:
                    text.set_fontsize(10)
                    text.set_fontweight('bold')
                
                ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                
                st.pyplot(fig)
                plt.close()
            
            with col2:
                # 상세 데이터 표시
                st.subheader("📋 상세 데이터")
                display_df = chart_data[['Genre', chart_column, 'Percentage']].copy()
                display_df.columns = ['장르', chart_column, '비율 (%)']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # 전체 상세 통계 표
        st.subheader("📈 전체 장르 통계")
        st.dataframe(detailed_df, use_container_width=True, hide_index=True)

    elif visualization == "인기 카테고리 분석":
        st.header("인기 카테고리 분석") 
        
        # 카테고리별 현재 접속자수 계산
        category_players = {}
        category_game_counts = {}
        
        for game in top100:
            appid = game["appid"]
            current_players = game.get("current_players", 0)
            
            # 메타데이터에서 카테고리 정보 가져오기
            meta = metadata.get(str(appid)) or metadata.get(appid) or {}
            categories = meta.get("categories", [])
            
            # 각 카테고리에 현재 접속자수 추가
            for category in categories:
                if category not in category_players:
                    category_players[category] = 0
                    category_game_counts[category] = 0
                category_players[category] += current_players
                category_game_counts[category] += 1
        
        # 상위 10개 카테고리 선택 (접속자수 기준)
        top_categories_by_players = sorted(category_players.items(), key=lambda x: x[1], reverse=True)[:10]
        top_categories_by_games = sorted(category_game_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 두 개의 컬럼으로 나누어 표시
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("카테고리별 현재 접속자수")
            if top_categories_by_players:
                category_players_df = pd.DataFrame(top_categories_by_players, columns=['Category', 'Current Players'])
                st.bar_chart(category_players_df.set_index('Category'))
                st.dataframe(category_players_df, use_container_width=True, hide_index=True)
            else:
                st.info("카테고리별 접속자수 데이터가 없습니다.")
        
        with col2:
            st.subheader("카테고리별 게임 수")
            if top_categories_by_games:
                category_games_df = pd.DataFrame(top_categories_by_games, columns=['Category', 'Game Count'])
                st.bar_chart(category_games_df.set_index('Category'))
                st.dataframe(category_games_df, use_container_width=True, hide_index=True)
            else:
                st.info("카테고리별 게임 수 데이터가 없습니다.")
        
        # 상세 통계
        st.subheader("카테고리별 상세 통계")
        detailed_stats = []
        for category in set(category_players.keys()) | set(category_game_counts.keys()):
            players = category_players.get(category, 0)
            games = category_game_counts.get(category, 0)
            avg_players = players / games if games > 0 else 0
            detailed_stats.append({
                'Category': category,
                'Total Players': players,
                'Game Count': games,
                'Avg Players per Game': round(avg_players, 1)
            })
        
        detailed_df = pd.DataFrame(detailed_stats).sort_values('Total Players', ascending=False)
        st.dataframe(detailed_df, use_container_width=True, hide_index=True)

    elif visualization == "게임 세부 검색":
        st.header("게임 세부 검색") 
        game_names = [meta.get("name", str(appid)) for appid, meta in metadata.items()]
        selected = st.selectbox("게임을 선택하세요:", game_names)
        # Find appid
        selected_appid = None
        for appid, meta in metadata.items():
            if meta.get("name", str(appid)) == selected:
                selected_appid = appid
                break
        if selected_appid:
            meta = metadata[selected_appid]
            st.subheader(meta.get("name", "Unknown"))
            st.write(f"**Genres:** {', '.join(meta.get('genres', []))}")
            st.write(f"**Categories:** {', '.join(meta.get('categories', []))}")
            st.write(f"**Release Date:** {meta.get('release_date', 'Unknown')}")
            st.write(f"**Price:** ${meta.get('price', 0):.2f}")
            st.write(meta.get("short_description", ""))
            if meta.get("header_image"):
                st.image(meta["header_image"], width=400)

if __name__ == "__main__":
    main()