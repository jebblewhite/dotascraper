import dotascraper

if __name__ == '__main__':
    d2scraper = dotascraper.DotaScraper()
    d2scraper.read_match_ids()
    d2scraper.read_json()
    print(len(d2scraper.match_ids))
    print(len(d2scraper.matches))

    while len(d2scraper.match_ids) > len(d2scraper.matches):
        d2scraper.get_matches()
    d2scraper.quitout()
