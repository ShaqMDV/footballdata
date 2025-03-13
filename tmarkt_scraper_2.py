from bs4 import BeautifulSoup
import requests

url = 'https://football.fandom.com/wiki/Lionel_Messi#Career_Statistics'# getting a single players stats just to test out the script functionality

# transfermarkt denied access, so going back to original source of data - fbref.com

# Could manually enter the missing data of players that were active pre-1988

page = requests.get(url)
print(page)

soup = BeautifulSoup(page.text, 'lxml')
print(soup.prettify())

