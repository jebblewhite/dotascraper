from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import json

class DotaScraper:
    BASE_URL = "https://www.opendota.com/matches/"
    def __init__(self,outfile='dotadata.json'):
        self.driver = webdriver.Chrome('./chromedriver')
        self.matches = []
        self.match_ids = []
        self.outfile = outfile
        
    def quitout(self):
        self.driver.quit()

    def get_match_ids(self):
        self.driver.get(self.BASE_URL)
        matches_container = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/div/div/div/table/tbody'))
        matches_full = matches_container.find_elements_by_xpath('./tr')
        self.match_ids = [match.text.split('\n')[0] for match in matches_full]
        try:
            self.dump_match_ids()
        except:
            self.create_match_ids()
        

    def get_matches(self):
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

    def parsed_ids_list(self):
        x = []
        [x.append(match["match_id"]) for match in self.matches if match["match_id"] in self.match_ids]
        return x

    def _check_if_not_parsed(self, match, parsed_ids):
        if match in parsed_ids:
            return False
        else:
            return True


    def get_match(self,match_id):
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
    def _picks_and_bans(picks,bans,pickbans):
        for pickban in pickbans:
                pickorban = pickban.find_element_by_xpath('./img').get_attribute('src').replace('https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/', '').replace('_sb.png', '')
                if "BAN" in pickban.text:
                    bans.append(pickorban)
                else:
                    picks.append(pickorban)
        return picks, bans
        

    def create_match_ids(self):
        with open('match_ids.json','w+') as file:
            json.dump(self.match_ids, file, indent = 4)

    def dump_match_ids(self):
        with open('match_ids.json','r+') as file:
            file_data = json.load(file)
            [self.match_ids.append(x) for x in file_data if x not in self.match_ids]
            file.seek(0)
            json.dump(self.match_ids, file, indent = 4)

    def read_match_ids(self):
        with open('match_ids.json','r+') as file:
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