import requests
from bs4 import BeautifulSoup
import csv

# Making a request to the website
url = "https://fbref.com/en/"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "lxml")

    # Extracting all links from the page
    links = soup.find_all("a")
    for link in links:
        print(link.get("href"))

    # Extract a specific element by class
    element = soup.find("div", class_="example_class")
    if element:
        print(element.text)

    # Writing football data to a CSV file
    with open("football_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Goals", "Assists"])

        # Extracting data from a table
        table = soup.find("table", class_="stats_table")
        if table:
            rows = table.find_all("tr")
            for row in rows:
                data = row.find_all("td")
                if len(data) > 2:
                    player = data[0].text.strip()
                    goals = data[1].text.strip()
                    assists = data[2].text.strip()
                    writer.writerow([player, goals, assists])
        else:
            print("Table not found")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
           