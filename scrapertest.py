import dotascraper

if __name__ == '__main__':
    d2scraper = dotascraper.DotaScraper()
    d2scraper.read_match_ids()
    d2scraper.get_matches(initial=False)
