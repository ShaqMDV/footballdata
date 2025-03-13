import requests
from bs4 import BeautifulSoup
import pandas as pd

# Making a request to the website
url = "https://football.fandom.com/wiki/Lionel_Messi#Career_Statistics"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')
table = soup.find_all('table')[3]

world_titles = soup.find_all('th') # Pulling out just the headers
world_table_titles = [title.text.strip() for title in world_titles] # looping through each header and retrieving its information

"""
When getting rid of the \n we can't just use strip() as we are working with a list
Instead we must put it within the for loop after 'title.text' for it to work
"""
df = pd.DataFrame(columns= world_table_titles)
df

column_data = table.find_all('tr')

for row in column_data[6:23]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    
    length = len(df)
    df.loc[length] = individual_row_data # This returned a mismatch error, which could be the result of empty sets being produced when running the above for loop

print(df)
# alternatively
# print (soup.find('table', class_ = "wikitable"))