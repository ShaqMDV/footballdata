
"""
Here we have the initial setup required using beautifulsoup and requests - here we have our desired web page being accessed through a request, when this is run we get all the HTML information supplied to us in the terminal below. Using prettify in the print statement allows us to display the information in a more readable format.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape (replace with the actual URL)
url = "https://www.transfermarkt.co.uk/martin-odegaard/profil/spieler/316264"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a GET request to the page
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract player name
    player_name = soup.find("h1", {"class": "data-header__headline-wrapper"}).text.strip()

    # Extract statistics (example: goals, assists, etc.)
    stats_table = soup.find("table", {"class": "items"})
    rows = stats_table.find_all("tr")

    data = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all("td")
        if len(columns) > 1:
            season = columns[0].text.strip()
            competition = columns[1].text.strip()
            goals = columns[6].text.strip()
            assists = columns[7].text.strip()
            data.append([player_name, season, competition, goals, assists])

    # Convert to a DataFrame
    df = pd.DataFrame(data, columns=["Player Name", "Season", "Competition", "Goals", "Assists"])

    # Save to CSV
    df.to_csv("player_stats.csv", index=False)
    print("Data saved to player_stats.csv")

    # Save to JSON
    df.to_json("player_stats.json", orient="records", lines=True)
    print("Data saved to player_stats.json")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")