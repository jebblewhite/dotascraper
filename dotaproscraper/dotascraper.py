"""
This module is a webscraper which runs on the OpenDota stats website. It has 2 main functions
    1. get the 100 most recent match IDs and output to file
    2. use the stored match IDs get the detailed match info and output to file
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import json

class DotaScraper:
    """
    This class is used for scraping data from the base URL.

    Attributes:
        driver (webdriver): The webdriver which will pilot Chrome (chromedriver file included in directory and must match user's Chrome app version)
        matches (list): a list of match dictionary items that will be dumped to json
        match_ids (list): a list of match id numbers that will be dumped to json
        outfile (str): the file name to output matches list to
    """
    BASE_URL = "https://www.opendota.com/matches/"
    def __init__(self, outfile: str='dotaproscraper/dotadata.json'):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.matches = []
        self.match_ids = []
        self.outfile = outfile
        
    def quitout(self):
        """
        Terminates the webdriver.
        """
        self.driver.quit()

    def get_match_ids(self):
        """
        Gets the match IDs from the most recent 100 professional games and outputs them to the match ID file.
        """
        self.driver.get(self.BASE_URL)
        matches_container = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/div/div/div/table/tbody'))
        matches_full = matches_container.find_elements_by_xpath('./tr')
        self.match_ids = [match.text.split('\n')[0] for match in matches_full]
        try:
            self.dump_match_ids()
        except:
            self.create_match_ids()
        

    def get_matches(self):
        """
        Reads the match ID file and gets the info for a batch of 100 matches.
        """
        self.read_match_ids()
        self.counter = 0
        self.read_json()
        parsed_matches = self.parsed_ids_list()
        for match in self.match_ids:
            if self._check_if_not_parsed(match, parsed_matches):
                self.get_match(match)
                self.counter += 1
            if self.counter >= 100:
                break
        try:
            self.write_json()
        except:
            self.create_json()

    def parsed_ids_list(self) -> list:
        """
        Checks the currently parsed matches against the ids to be scraped.

        Returns:
            x (list): the list of match IDs that have already been scraped and outputed
        """
        x = []
        [x.append(match["match_id"]) for match in self.matches if match["match_id"] in self.match_ids]
        return x

    def _check_if_not_parsed(self, match: str, parsed_ids: list) -> bool:
        """
        Checks if individual match has been parsed

        Arguments:
            match (str): Match ID to potentially scrape from
            parsed_ids (list): list of parsed IDs to reference

        Returns:
            bool : False if in the list, will not parse already parsed data
        """
        if match in parsed_ids:
            return False
        else:
            return True


    def get_match(self, match_id: str):
        """
        Scrapes OpenDota for specified match ID, saves data to dictionary and appends dictionary to matches list

        Arguments:
            match (str): Match ID to scrape data from
        """
        self.driver.get(self.BASE_URL+match_id)
        header = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/header/div[1]'))
        header_list = header.text.split('\n')
        winner_name = header_list[0].replace(' Victory', '')
        # only looking at captains mode games
        if header_list[2] == 'CAPTAINS MODE':
            match_dict_item = {}
            match_dict_item['match_id'] = match_id
            # find the picks and bans for both teams by finding their elements
            radiant_pickbans_container = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[1]/div[3]/div')
            dire_pickbans_container = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[1]/div[6]/div')
            radiant_pickbans = radiant_pickbans_container.find_elements_by_xpath('./section')
            dire_pickbans = dire_pickbans_container.find_elements_by_xpath('./section')
            # determine winning side by name featuring both in header and team container
            if winner_name in self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[1]/div[1]/span[1]').text:
                winner = "radiant"
            else:
                winner = "dire"

            match_dict_item['winner'] = winner

            radiant_picks = []
            dire_picks = []
            bans = []

            radiant_picks, bans = self._picks_and_bans(radiant_picks, bans, radiant_pickbans)
            dire_picks, bans = self._picks_and_bans(dire_picks, bans, dire_pickbans)

            match_dict_item['radiant_picks'] = radiant_picks
            match_dict_item['dire_picks'] = dire_picks
            match_dict_item['bans'] = bans
            self.matches.append(match_dict_item)
    
    @staticmethod
    def _picks_and_bans(picks: list, bans: list, pickbans: list) -> list:
        """
        A static method which sorts picks from bans based on text data.

        Arguments:
            picks (list): empty list 
            bans (list): empty list or list with 5 hero bans
            pickbans (list): a list of 5 picks and 5 bans

        Returns:
            picks (list): list of 5 hero picks
            bans (list): list of 5 or 10 hero bans
        """
        for pickban in pickbans:
                pickorban = pickban.find_element_by_xpath('./img').get_attribute('src').replace('https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/', '').replace('_sb.png', '')
                if "BAN" in pickban.text:
                    bans.append(pickorban)
                else:
                    picks.append(pickorban)
        return picks, bans
        

    def create_match_ids(self):
        with open('dotaproscraper/match_ids.json','w+') as file:
            json.dump(self.match_ids, file, indent = 4)

    def dump_match_ids(self):
        with open('dotaproscraper/match_ids.json','r+') as file:
            file_data = json.load(file)
            [self.match_ids.append(x) for x in file_data if x not in self.match_ids]
            file.seek(0)
            json.dump(self.match_ids, file, indent = 4)

    def read_match_ids(self):
        with open('dotaproscraper/match_ids.json','r+') as file:
            file_data = json.load(file)
            [self.match_ids.append(x) for x in file_data if x not in self.match_ids]

    def create_json(self):
        with open(self.outfile,'w+') as file:
            matchdict = {'matches':self.matches}
            json.dump(matchdict, file, indent = 4)

    def write_json(self):
        with open(self.outfile,'r+') as file:
            file_data = json.load(file)
            [self.matches.append(x) for x in file_data["matches"] if x not in self.matches]
            matchdict = {'matches':self.matches}
            file.seek(0)
            json.dump(matchdict, file, indent = 4)
    
    def read_json(self):
        with open(self.outfile,'r+') as file:
            file_data = json.load(file)
            [self.matches.append(x) for x in file_data["matches"] if x not in self.matches]

if __name__ == '__main__':
    d2scraper = DotaScraper()
    d2scraper.get_match_ids()