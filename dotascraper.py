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
        self.driver.get(self.BASE_URL)
        sleep(2)
        if initial:
            matches_container = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/div/div/div/table/tbody')
            matches_full = matches_container.find_elements_by_xpath('./tr')
            self.match_ids = [match.text.split('\n')[0] for match in matches_full]
            try:
                self.dump_match_ids()
            except:
                self.create_match_ids()

    def get_match(self,match_id):
        self.driver.get(self.BASE_URL+match_id)
        sleep(2)
        header = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/header/div[1]')
        header_list = header.text.split('\n')
        print(header_list)
        if header_list[2] == 'CAPTAINS MODE':
            radiant_pickbans = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[1]/div[3]/div')
            dire_pickbans = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[1]/div[6]/div')
            print(radiant_pickbans.text)


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
            json.dump(self.matches, file, indent = 4)

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