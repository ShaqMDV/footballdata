import requests
from bs4 import BeautifulSoup
import csv

"""
This script demonstrates how to scrape raw HTML content from a website using the requests library and the BeautifulSoup library.
"""
# Making a request to the website

url = "https://fbref.com/en/"
response = requests.get(url)
print(response.text) # prints the raw HTML content of the page

# Parsing the raw HTML content using BeautifulSoup

soup = BeautifulSoup(response.text, "lxml")
print(soup.prettify()) # prints the HTML content in a more readable format

# Extracting all links from the page

"""
Locate specific elements on the page using CSS selectors or HTML tags
"""

links = soup.find_all("a") # finds all <a> tags in the HTML content
for link in links:
    print(link.get("href")) # prints the value of the "href" attribute for each link

# Extract a specific element by class
element = soup.find("div", class_="example_class")
print(element.txt) # Extracts the text inside the element

with open(football_data.csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Player", "Goals", "Assists"])
    # Extracting data from a table
    table = soup.find("table", class_="stats_table")
    rows = table.find_all("tr")
    for row in rows:
        data = row.find_all("td")
        if len(data) > 0:
            player = data[0].text
            goals = data[1].text
            assists = data[2].text
            writer.writerow([player, goals, assists])