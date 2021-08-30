# dotascraper
A DotA 2 Professional Match Webscraper


The aim of this project is to take data from opendota's recent matches and store the match ids to be accessed individually for more in-depth data: team picks, team bans, and which team won. By taking this information, trends on hero pickrate, banrate, and winrate can be established. There is potential in future to predict which team will win a given match based on picks, as DotA is a highly competitive game and often the best picks can be the deciding factor.

dotascraper.py contains the scraper class, to be used for data capture, cleaning and analysis.

match_ids.json contains match ids for scraping

scrapertest.py is a test sraping object

dotadata.json is the final output, ready to be analysed



requirements:
  python 3.9.6
  selenium 3.141.0
  time
  json
  chromdriver (included in repo)
