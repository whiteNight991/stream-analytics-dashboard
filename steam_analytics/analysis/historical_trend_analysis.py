import os
import json
from datetime import datetime, timedelta
import pandas as pd

def load_historical_top100_data(months_ago: int = 3):
    raw_data_dir = "data/raw"
    
    historical_data_by_month = {}
    
    # List all files in the raw data directory
    if os.path.exists(raw_data_dir):
        all_files = os.listdir(raw_data_dir)
        json_files = [f for f in all_files if f.startswith("top100_games_") and f.endswith(".json")]
        json_files.sort() # Sort to ensure chronological order

        print(f"🔍 Found JSON files: {json_files}")
        
        for filename in json_files:
            filepath = os.path.join(raw_data_dir, filename)
            try:
                # Parse date from filename (YYYYMM or YYYYMMDD format)
                date_part = filename.split("_")[-1].split(".")[0] # YYYYMM or YYYYMMDD
                
                # Try parsing as YYYYMMDD first, then YYYYMM
                file_date = None
                if len(date_part) == 8: # YYYYMMDD
                    file_date = datetime.strptime(date_part, "%Y%m%d")
                elif len(date_part) == 6: # YYYYMM
                    file_date = datetime.strptime(date_part, "%Y%m")
                else:
                    print(f"Skipping {filename}: Unrecognized date format in filename.")
                    continue
                
                month_year_key = file_date.strftime('%Y년 %m월')
                
                print(f"📁 Loading file: {filename} -> Date: {month_year_key}")
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for game in data:
                        game['timestamp'] = file_date  # Add timestamp to each game entry

                    if month_year_key not in historical_data_by_month:
                        historical_data_by_month[month_year_key] = []
                    historical_data_by_month[month_year_key].extend(data)
                print(f"✅ Loaded {len(data)} games from {filename} (Date: {month_year_key})")
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
    else:
        print(f"❌ Directory not found: {raw_data_dir}")

    print(f"📊 Total loaded months: {len(historical_data_by_month)}")
    
    return historical_data_by_month

def analyze_player_trends(historical_data: list) -> pd.DataFrame:
    # Convert to DataFrame
    df = pd.DataFrame(historical_data)

    if df.empty:
        return pd.DataFrame()

    # Ensure appid is string for consistent merging later if needed
    try:
        df['appid'] = df['appid'].astype(str)
    except Exception as e:
        print(f"Error converting appid to string: {e}")
        return pd.DataFrame()

    # Handle both 'current_players' and 'avg_players' fields
    if 'current_players' in df.columns:
        player_column = 'current_players'
    elif 'avg_players' in df.columns:
        player_column = 'avg_players'
    else:
        print("No player count column found (neither 'current_players' nor 'avg_players')")
        return pd.DataFrame()

    try:
        # Pivot table to get player counts over time for each game
        # Filter to only include games that appear frequently or have high player counts
        # For simplicity, let's just get the average player count over time for each game that appears
        
        # Group by appid and timestamp to get average players per game per snapshot
        trend_df = df.groupby(['appid', pd.Grouper(key='timestamp', freq='D')])[player_column].mean().unstack(level=0)
        
        # Interpolate missing values to show continuous trends
        trend_df = trend_df.interpolate(method='linear', limit_direction='both')
        
        return trend_df
    except Exception as e:
        print(f"Error in trend analysis: {e}")
        return pd.DataFrame()

def get_top_n_consistent_games(historical_data: list, n: int = 10) -> list:
    try:
        df = pd.DataFrame(historical_data)
        if df.empty:
            return []
        # Count how many times each game appears in the top 100 over the period
        game_counts = df['appid'].value_counts()
        # Get appids of top N most consistently appearing games
        top_n_appids = game_counts.head(n).index.tolist()
        
        # Convert to string to match trend_df column format
        top_n_appids_str = [str(appid) for appid in top_n_appids]
        return top_n_appids_str
    except Exception as e:
        print(f"Error getting consistent games: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    historical_data = load_historical_top100_data(months_ago=1) # Load data for last 1 month
    if historical_data:
        print(f"Loaded {len(historical_data)} game entries from the last month.")
        trend_df = analyze_player_trends(historical_data)
        if not trend_df.empty:
            print("\nPlayer Trend Data (first 5 rows):")
            print(trend_df.head())
        else:
            print("No trend data generated.")

        top_games_consistent = get_top_n_consistent_games(historical_data, 5)
        print(f"\nTop 5 most consistently appearing games (AppIDs): {top_games_consistent}")
    else:
        print("No historical data found for the last month.") 