from bs4 import BeautifulSoup as soup, Comment
import requests
import pandas as pd
import time
import sys
from urllib.error import HTTPError

"""
This script scrapes seasonal player statistics (including goalkeeping, shooting, and advanced stats)
for a selected league and season from FBRef.
"""

# Base URL
base_url = "https://fbref.com"

# Headers to mimic a real browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_data_info():
    leagues = ['Premier League', 'La Liga', 'Serie A', 'Ligue 1', 'Bundesliga']
    seasons = [f"{year}-{year+1}" for year in range(2017, 2024)]  # xG data is only available from 2017

    while True:
        league = input('Select League (Premier League / La Liga / Serie A / Ligue 1 / Bundesliga): ')
        if league not in leagues:
            print('League not valid, try again')
            continue
        
        league_mapping = {
            'Premier League': ('Premier-League', '9'),
            'La Liga': ('La-Liga', '12'),
            'Serie A': ('Serie-A', '11'),
            'Ligue 1': ('Ligue-1', '13'),
            'Bundesliga': ('Bundesliga', '20')
        }
        league, league_id = league_mapping[league]
        break

    while True:
        season = input(f'Select Season ({", ".join(seasons)}): ')
        if season not in seasons:
            print('Season not valid, try again')
            continue
        break

    url = f"https://fbref.com/en/comps/{league_id}/{season}/stats/{season}-{league}-Stats"
    return url, league, season

def get_player_links(url):
    print('Fetching player profile links...')
    
    html = requests.get(url, headers=headers)
    if html.status_code != 200:
        print("Failed to fetch the stats page!")
        return []

    page_soup = soup(html.content, "html.parser")

    # Extract tables from HTML comments
    for comment in page_soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment_soup = soup(comment, 'html.parser')
        for table in comment_soup.find_all("table", id="stats_standard"):
            page_soup.append(table)  # Append to the main page soup

    player_links = []

    # Find player profile links
    for row in page_soup.select("table#stats_standard tbody tr"):
        link_tag = row.find("th", {"data-stat": "player"}).find("a")
        if link_tag:
            player_links.append((link_tag.text, base_url + link_tag['href']))

    if not player_links:
        print("No player links found! The page structure might have changed.")
    else:
        print(f"Found {len(player_links)} players.")

    return player_links


def extract_stat(row, stat):
    """ Helper function to safely extract data from table rows """
    cell = row.find(["th", "td"], {"data-stat": stat})
    return cell.text.strip() if cell else "0"

def scrape_player_stats(player_links, league, season):
    print('Scraping player statistics...')
    player_data = []

    for count, (name, profile_url) in enumerate(player_links):
        print(f"Scraping {name} ({count+1}/{len(player_links)})")
        player_response = requests.get(profile_url, headers=headers)

        if player_response.status_code != 200:
            print(f"Failed to fetch {name}'s profile")
            continue

        player_soup = soup(player_response.text, 'html.parser')

        # Extract tables hidden inside HTML comments
        for comment in player_soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment_soup = soup(comment, 'html.parser')
            for table in comment_soup.find_all("table"):
                player_soup.append(table)

        # Define tables
        stats_table = player_soup.find("table", id="stats_standard")
        shooting_table = player_soup.find("table", id="stats_shooting")
        keeper_table = player_soup.find("table", id="stats_keeper")
        advanced_table = player_soup.find("table", id="stats_adv")

        if stats_table:
            for row in stats_table.find("tbody").find_all("tr"):
                season_year = extract_stat(row, "season")
                league_name = extract_stat(row, "league")
                games = extract_stat(row, "games")
                goals = extract_stat(row, "goals")
                assists = extract_stat(row, "assists")

                # Shooting stats
                shots, shots_on_target, shot_accuracy, xg = "0", "0", "0", "0"
                if shooting_table:
                    shooting_row = shooting_table.find("tr", {"id": row.get("id")})
                    if shooting_row:
                        shots = extract_stat(shooting_row, "shots")
                        shots_on_target = extract_stat(shooting_row, "shots_on_target")
                        shot_accuracy = extract_stat(shooting_row, "shots_on_target_pct")
                        xg = extract_stat(shooting_row, "xg")

                # Goalkeeper stats
                saves, clean_sheets, save_pct = "0", "0", "0"
                if keeper_table:
                    keeper_row = keeper_table.find("tr", {"id": row.get("id")})
                    if keeper_row:
                        saves = extract_stat(keeper_row, "saves")
                        clean_sheets = extract_stat(keeper_row, "clean_sheets")
                        save_pct = extract_stat(keeper_row, "save_pct")

                # Advanced stats
                xg_per_90, xa_per_90, pass_completion = "0", "0", "0"
                if advanced_table:
                    adv_row = advanced_table.find("tr", {"id": row.get("id")})
                    if adv_row:
                        xg_per_90 = extract_stat(adv_row, "xg_per90")
                        xa_per_90 = extract_stat(adv_row, "xa_per90")
                        pass_completion = extract_stat(adv_row, "passes_completed_pct")

                # Store player stats
                player_data.append({
                    "Player": name,
                    "Season": season_year,
                    "League": league_name,
                    "Games": games,
                    "Goals": goals,
                    "Assists": assists,
                    "Shots": shots,
                    "Shots on Target": shots_on_target,
                    "Shot Accuracy %": shot_accuracy,
                    "xG": xg,
                    "Saves": saves,
                    "Clean Sheets": clean_sheets,
                    "Save %": save_pct,
                    "xG per 90": xg_per_90,
                    "xA per 90": xa_per_90,
                    "Pass Completion %": pass_completion,
                    "Profile URL": profile_url
                })

        time.sleep(2)  # Pause to avoid IP blocking

    df = pd.DataFrame(player_data)
    if not df.empty:
        df.to_csv(f"{league.lower()}_{season.lower()}_player_stats.csv", index=False)
        print("Data saved successfully!")
    else:
        print("No data was scraped! Check FBRef structure.")

def main():
    url, league, season = get_data_info()
    player_links = get_player_links(url)
    
    if not player_links:
        print("No player links found. Exiting...")
        sys.exit()

    scrape_player_stats(player_links, league, season)

    print("Data collection complete!")

    while True:
        answer = input("Do you want to collect more data? (yes/no): ")
        if answer.lower() == 'yes':
            main()
        elif answer.lower() == 'no':
            sys.exit()
        else:
            print("Invalid answer, try again.")

if __name__ == '__main__':
    try:
        main()
    except HTTPError:
        print("The website refused access, try again later")
        time.sleep(5)


