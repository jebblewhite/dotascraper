"""
This module contains a scraper and database creator, which finds a number of Dota 2 Professional Match IDs, and extracts key information, outputs it to file and then
transforms the data into a readable, analysable format.
"""
from .dotascraper import DotaScraper
from .databaser import Databaser

if __name__ == "__main__":
    print("Initialising Scraper...", end='')
    d2scraper = DotaScraper()
    print("Done.")
    print("Fetching Match IDs...", end='')
    d2scraper.get_match_ids()
    print("Done.")
    d2scraper.read_json()

    print("Scraping matches...", end='')
    try:
        while len(d2scraper.match_ids) > len(d2scraper.matches):
            d2scraper.get_matches()
    except:
        d2scraper.quitout()
        print("Done.")

    print("Initialising Database...", end='')
    db = Databaser()
    print("Done.")
    print("Pushing data to Database...", end='')
    db.push_to_db(db.df, "dota_dataset")
    print("Done.") 
    print("Analysing hero rates and pushing data to Database...", end='')
    db.analyse_rates()
    print("Done.")
    print("Please access the database using pgAdmin to see the results.") 