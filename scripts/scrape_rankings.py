"""
Scrape fantasy baseball rankings from various sources.

Options:
1. FantasyPros (recommended - aggregates multiple sources including ESPN)
2. ESPN directly (requires authentication for some features)

Usage:
    python scripts/scrape_rankings.py fantasypros
    python scripts/scrape_rankings.py espn
"""

import argparse
import pandas as pd
import time
import os

# Try to import selenium, provide install instructions if not available
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def scrape_fantasypros():
    """
    Scrape FantasyPros consensus rankings.
    These aggregate rankings from ESPN, CBS, Yahoo, and other experts.
    """
    if not SELENIUM_AVAILABLE:
        print("Selenium not installed. Install with: pip install selenium")
        print("You also need ChromeDriver: https://chromedriver.chromium.org/downloads")
        return None

    print("Scraping FantasyPros rankings...")

    # Set up headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error starting Chrome: {e}")
        print("Make sure ChromeDriver is installed and in PATH")
        return None

    try:
        # Load the rankings page
        url = "https://www.fantasypros.com/mlb/rankings/overall.php"
        driver.get(url)

        # Wait for the table to load
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.player-table")))

        # Give it a moment for all data to load
        time.sleep(2)

        # Find all player rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table.player-table tbody tr")

        players = []
        for row in rows:
            try:
                # Get rank
                rank_elem = row.find_element(By.CSS_SELECTOR, "td.rank-cell")
                rank = rank_elem.text.strip()

                # Get player name
                name_elem = row.find_element(By.CSS_SELECTOR, "td.player-cell a.player-name")
                name = name_elem.text.strip()

                # Get team and position
                info_elem = row.find_element(By.CSS_SELECTOR, "td.player-cell small")
                info = info_elem.text.strip()  # e.g., "NYY - OF"

                parts = info.split(" - ")
                team = parts[0] if len(parts) > 0 else ""
                position = parts[1] if len(parts) > 1 else ""

                players.append({
                    'FP_Rank': int(rank) if rank.isdigit() else rank,
                    'Name': name,
                    'Team': team,
                    'Position': position
                })
            except Exception as e:
                continue

        driver.quit()

        if players:
            df = pd.DataFrame(players)
            print(f"Scraped {len(df)} players")
            return df
        else:
            print("No players found")
            return None

    except Exception as e:
        print(f"Error scraping: {e}")
        driver.quit()
        return None


def scrape_espn_projections():
    """
    Scrape ESPN fantasy baseball projections/rankings.
    Note: Full rankings may require ESPN+ subscription.
    """
    if not SELENIUM_AVAILABLE:
        print("Selenium not installed. Install with: pip install selenium")
        return None

    print("Scraping ESPN projections...")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error starting Chrome: {e}")
        return None

    try:
        # ESPN Fantasy Baseball Players page
        url = "https://fantasy.espn.com/baseball/players/projections"
        driver.get(url)

        # Wait for player table
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

        time.sleep(3)

        # Find player rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        players = []
        rank = 1
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    # First cell usually has player info
                    name_cell = cells[0]
                    name = name_cell.text.split('\n')[0].strip()

                    if name and not name.startswith('--'):
                        players.append({
                            'ESPN_Rank': rank,
                            'Name': name,
                        })
                        rank += 1
            except:
                continue

        driver.quit()

        if players:
            df = pd.DataFrame(players)
            print(f"Scraped {len(df)} players")
            return df
        else:
            print("No players found - ESPN may require login")
            return None

    except Exception as e:
        print(f"Error scraping ESPN: {e}")
        driver.quit()
        return None


def manual_entry_template():
    """
    Create a template CSV for manual entry of ESPN rankings.
    """
    template = pd.DataFrame({
        'ESPN_Rank': range(1, 301),
        'Name': [''] * 300,
        'Team': [''] * 300,
        'Position': [''] * 300
    })

    path = 'data/espn/espn_rankings_template.csv'
    os.makedirs('data/espn', exist_ok=True)
    template.to_csv(path, index=False)
    print(f"Created template at {path}")
    print("Fill in player names from ESPN draft room and save as espn_rankings_2026.csv")
    return path


def main():
    parser = argparse.ArgumentParser(description='Scrape fantasy baseball rankings')
    parser.add_argument('source', choices=['fantasypros', 'espn', 'template'],
                        help='Source to scrape (fantasypros, espn) or create template')
    parser.add_argument('--output', '-o', default=None,
                        help='Output CSV path')

    args = parser.parse_args()

    os.makedirs('data/espn', exist_ok=True)

    if args.source == 'fantasypros':
        df = scrape_fantasypros()
        if df is not None:
            output = args.output or 'data/espn/fantasypros_rankings_2026.csv'
            df.to_csv(output, index=False)
            print(f"Saved to {output}")

    elif args.source == 'espn':
        df = scrape_espn_projections()
        if df is not None:
            output = args.output or 'data/espn/espn_rankings_2026.csv'
            df.to_csv(output, index=False)
            print(f"Saved to {output}")
        else:
            print("\nESPN scraping failed. Alternatives:")
            print("1. Use FantasyPros (includes ESPN expert): python scripts/scrape_rankings.py fantasypros")
            print("2. Create manual template: python scripts/scrape_rankings.py template")

    elif args.source == 'template':
        manual_entry_template()


if __name__ == "__main__":
    main()
