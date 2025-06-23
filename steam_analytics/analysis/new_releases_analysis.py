import os
import json
from datetime import datetime
import pandas as pd
from pathlib import Path

def load_monthly_new_releases_data():
    """
    월별 인기 출시 게임 데이터를 로드합니다.
    """
    raw_data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    
    monthly_data = {}
    
    if raw_data_dir.exists():
        all_files = os.listdir(raw_data_dir)
        new_releases_files = [f for f in all_files if f.startswith("new_releases_") and f.endswith(".json")]
        new_releases_files.sort()
        
        print(f"🔍 Found new releases files: {new_releases_files}")
        
        for filename in new_releases_files:
            filepath = raw_data_dir / filename
            try:
                # 파일명에서 월 정보 추출 (new_releases_march_2025_20250617_114950.json)
                parts = filename.replace("new_releases_", "").replace(".json", "").split("_")
                if len(parts) >= 2:
                    month_name = parts[0]  # march, april, may
                    year = parts[1]        # 2025
                    
                    # 월 이름을 한글로 변환
                    month_mapping = {
                        "march": "3월",
                        "april": "4월", 
                        "may": "5월"
                    }
                    
                    month_key = f"{year}년 {month_mapping.get(month_name, month_name)}"
                    
                    print(f"📁 Loading file: {filename} -> Month: {month_key}")
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    if month_key not in monthly_data:
                        monthly_data[month_key] = []
                    monthly_data[month_key].extend(data)
                    
                    print(f"✅ Loaded {len(data)} new release games from {filename}")
                    
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
    else:
        print(f"❌ Directory not found: {raw_data_dir}")
    
    print(f"📊 Total loaded months: {len(monthly_data)}")
    
    return monthly_data

def analyze_new_releases_by_month(monthly_data, selected_month):
    """
    선택된 월의 인기 출시 게임을 분석합니다.
    """
    if selected_month not in monthly_data:
        return None
    
    month_data = monthly_data[selected_month]
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(month_data)
    
    if df.empty:
        return None
    
    # 태그 분석
    all_tags = []
    for tags in df.get('tags', []):
        if isinstance(tags, list):
            all_tags.extend(tags)
        elif isinstance(tags, str):
            all_tags.extend([tag.strip() for tag in tags.split(',')])
    
    tag_counts = pd.Series(all_tags).value_counts().head(10)
    
    # 평점 분석
    rating_counts = df.get('rating', []).value_counts() if 'rating' in df.columns else pd.Series()
    
    return {
        'total_games': len(df),
        'top_tags': tag_counts.to_dict(),
        'rating_distribution': rating_counts.to_dict(),
        'games_data': df.to_dict('records')
    }

def get_top_new_releases(monthly_data, selected_month, top_n=10):
    """
    선택된 월의 상위 인기 출시 게임을 반환합니다.
    """
    if selected_month not in monthly_data:
        return []
    
    month_data = monthly_data[selected_month]
    
    # 랭킹 순으로 정렬
    sorted_games = sorted(month_data, key=lambda x: x.get('rank', 999))
    
    return sorted_games[:top_n]

if __name__ == "__main__":
    # 테스트
    monthly_data = load_monthly_new_releases_data()
    print(f"Available months: {list(monthly_data.keys())}")
    
    if monthly_data:
        for month in monthly_data.keys():
            print(f"\n📅 Analyzing {month}:")
            analysis = analyze_new_releases_by_month(monthly_data, month)
            if analysis:
                print(f"Total games: {analysis['total_games']}")
                print(f"Top tags: {list(analysis['top_tags'].keys())[:5]}") 