from .dotascraper import DotaScraper
from .databaser import Databaser

if __name__ == "__main__":
    d2scraper = DotaScraper()
    d2scraper.get_match_ids()
    d2scraper.read_json()
    try:
        while len(d2scraper.match_ids) > len(d2scraper.matches):
            d2scraper.get_matches()
    except:
        d2scraper.quitout()

    db = Databaser()
    db.push_to_db(db.df, "dota_dataset")  
    db.analyse_rates()  