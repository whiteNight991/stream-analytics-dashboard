from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
from typing import Dict, Optional
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Initializes a new Selenium WebDriver instance using a local chromedriver."""
    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Use the local chromedriver
        driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
        if not os.path.exists(driver_path):
            print(f"ChromeDriver not found at {driver_path}")
            print("Please download the correct version of ChromeDriver for your system and place it in the 'steam_analytics/scraper' directory.")
            return None

        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver with local chromedriver: {e}")
        return None

def get_country_stats(driver, country_code: str) -> Optional[Dict]:
    """Get country-specific statistics from Steam Charts."""
    base_url = "https://store.steampowered.com/charts/topselling"
    try:
        url = f"{base_url}/{country_code.lower()}"
        driver.get(url)
        time.sleep(7)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        stats = {
            "country_code": country_code,
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "top_sellers": []
        }

        rows = soup.select('tr[class*="salepreviewwidgets_SaleItemBrowserRow_"]')

        for row in rows:
            link_tag = row.select_one('a[href*="/app/"]')
            if not link_tag:
                continue

            href = link_tag['href']
            match = re.search(r'/app/(\d+)/', href)
            if not match:
                continue
            game_id = match.group(1)

            name_tag = row.select_one('div[class*="salepreviewwidgets_StoreSaleWidgetTitle_"]')
            game_name = name_tag.get_text(strip=True) if name_tag else "Unknown"
            
            if not any(d.get('id') == int(game_id) for d in stats["top_sellers"]):
                stats["top_sellers"].append({
                    "id": int(game_id),
                    "name": game_name,
                })

            if len(stats["top_sellers"]) >= 10:
                break
        
        return stats
        
    except Exception as e:
        print(f"Error fetching stats for {country_code}: {str(e)}")
        return None

def save_to_json(data: Dict, filename: str):
    """Save data to a JSON file."""
    os.makedirs("data/raw/country_stats", exist_ok=True)
    filepath = os.path.join("data/raw/country_stats", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # 드롭다운을 이용해 대한민국을 선택하는 디버그 코드
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import time
    import os

    chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        url = "https://store.steampowered.com/charts/topselling"
        print(f"[DEBUG] Opening {url}")
        driver.get(url)
        time.sleep(3)
        # 드롭다운 버튼 클릭
        dropdown_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.DialogDropDown'))
        )
        dropdown_btn.click()
        time.sleep(1)
        # 모든 국가 옵션 추출
        options = driver.find_elements(By.CSS_SELECTOR, '.DialogDropDown_Option')
        print(f"[DEBUG] Found {len(options)} country options:")
        for idx, opt in enumerate(options):
            print(f"  {idx+1}. {opt.text}")
        # (자동화 확장: 이후 각 옵션 클릭 및 데이터 추출 가능)
        # 예시: 첫 번째 옵션 클릭
        # options[0].click()
        # time.sleep(3)
        # ... 데이터 추출 ...
    finally:
        driver.quit()

    all_country_stats = {}
    countries = [
        "KR", "US", "JP", "CN", "GB", "DE", "FR", "RU", "BR", "IN",
        "CA", "AU", "SG", "TW", "HK", "TH", "ID", "MY", "PH", "VN"
    ]
    
    print("Fetching country statistics from Steam Charts using local chromedriver...")
    for country in countries:
        print(f"Processing {country}...")
        driver = init_driver()
        if not driver:
            print(f"Failed to start WebDriver for {country}. Skipping.")
            continue
        
        stats = get_country_stats(driver, country)
        if stats and stats["top_sellers"]:
            all_country_stats[country] = stats
            print(f"Successfully fetched {len(stats['top_sellers'])} games for {country}.")
        else:
            print(f"No data found for {country}.")
        
        driver.quit()
        time.sleep(3)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_json(all_country_stats, f"country_stats_{timestamp}.json")
    print(f"Successfully saved country statistics to data/raw/country_stats/country_stats_{timestamp}.json")

if __name__ == "__main__":
    main()
