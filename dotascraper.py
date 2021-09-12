from selenium import webdriver
from time import sleep
import json

class DotaScraper:
    BASE_URL = "https://www.opendota.com/matches/"
    def __init__(self,outfile='dotadata.json'):
        self.driver = webdriver.Chrome()
        self.matches = []
        self.match_ids = []
        self.outfile = outfile

    def get_matches(self, initial=True):
        if initial:
            self.driver.get(self.BASE_URL)
            sleep(2)
            matches_container = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/div/div/div/table/tbody')
            matches_full = matches_container.find_elements_by_xpath('./tr')
            self.match_ids = [match.text.split('\n')[0] for match in matches_full]
            try:
                self.dump_match_ids()
            except:
                self.create_match_ids()

        else:
            self.read_match_ids()
            for match in self.match_ids:
                self.get_match(match)
            try:
                self.write_json()
            except:
                self.create_json()

    def get_match(self,match_id):
        self.driver.get(self.BASE_URL+match_id)
        try:
            sleep(1)
            # find the winner of the match from the header
            header = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/header/div[1]')
        except:
            sleep(5)
            header = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/header/div[1]')
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

            for pickbans in radiant_pickbans:
                pickorban = pickbans.find_element_by_xpath('./img').get_attribute('src').replace('https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/', '').replace('_sb.png', '')
                if "BAN" in pickbans.text:
                    bans.append(pickorban)
                else:
                    radiant_picks.append(pickorban)

            for pickbans in dire_pickbans:
                pickorban = pickbans.find_element_by_xpath('./img').get_attribute('src').replace('https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/', '').replace('_sb.png', '')
                if "BAN" in pickbans.text:
                    bans.append(pickorban)
                else:
                    dire_picks.append(pickorban)
            match_dict_item['radiant_picks'] = radiant_picks
            match_dict_item['dire_picks'] = dire_picks
            match_dict_item['bans'] = bans
            self.matches.append(match_dict_item)
        

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

if __name__ == '__main__':
    d2scraper = DotaScraper()
    d2scraper.get_matches()