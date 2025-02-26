import scrapy
import re
from bs4 import BeautifulSoup

class FBRefSpider(scrapy.Spider):
    name = "fbref"
    allowed_domains = ["fbref.com"]
    base_url = "https://fbref.com"

    def start_requests(self):
        """ Prompt user for league & season, then fetch fixture list. """
        leagues = {
            'Premier League': ('Premier-League', '9'),
            'La Liga': ('La-Liga', '12'),
            'Serie A': ('Serie-A', '11'),
            'Ligue 1': ('Ligue-1', '13'),
            'Bundesliga': ('Bundesliga', '20')
        }
        
        league_name = input('Select League (Premier League / La Liga / Serie A / Ligue 1 / Bundesliga): ')
        season = input('Select Season (e.g. 2023-2024): ')

        if league_name not in leagues:
            self.logger.error("Invalid league selected!")
            return

        league_url, league_id = leagues[league_name]
        url = f"{self.base_url}/en/comps/{league_id}/{season}/schedule/{season}-{league_url}-Scores-and-Fixtures"
        
        yield scrapy.Request(url=url, callback=self.parse_fixtures, meta={'league': league_name, 'season': season})

    def parse_fixtures(self, response):
        """ Extract match URLs from the fixture page. """
        matches = response.css("table#sched_advanced tbody tr")

        for match in matches:
            match_link = match.css("th[data-stat='score'] a::attr(href)").get()
            if match_link:
                full_link = response.urljoin(match_link)
                yield scrapy.Request(full_link, callback=self.parse_match, meta=response.meta)

    def parse_match(self, response):
        """ Extract player stats from each match page, including hidden tables. """
        league = response.meta['league']
        season = response.meta['season']
        match_id = response.url.split("/")[-1]

        # Extract raw HTML comments where tables are hidden
        soup = BeautifulSoup(response.text, "html.parser")
        comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith("<!--"))

        # Extract tables from comments
        extracted_tables = []
        for comment in comments:
            comment_soup = BeautifulSoup(comment, "html.parser")
            extracted_tables.extend(comment_soup.find_all("table"))

        # Standard, Shooting, and Advanced Stats Tables
        table_ids = {
            "standard": "stats_standard",
            "shooting": "stats_shooting",
            "goalkeeping": "stats_keeper",
            "advanced": "stats_adv"
        }

        for stat_type, table_id in table_ids.items():
            table = None

            # Search for table in extracted HTML comments
            for extracted_table in extracted_tables:
                if extracted_table.get("id") == table_id:
                    table = extracted_table
                    break

            if table:
                for row in table.find("tbody").find_all("tr"):
                    player_link_tag = row.find("th", {"data-stat": "player"}).find("a")
                    if not player_link_tag:
                        continue

                    player_name = player_link_tag.text.strip()
                    player_link = response.urljoin(player_link_tag["href"])

                    stats = {}
                    for cell in row.find_all("td"):
                        stat_name = cell.get("data-stat")
                        stat_value = cell.text.strip() or "0"
                        stats[stat_name] = stat_value

                    stats.update({
                        "player": player_name,
                        "match_id": match_id,
                        "season": season,
                        "league": league,
                        "player_link": player_link,
                        "stat_type": stat_type
                    })

                    yield stats
