from selenium import webdriver
from time import sleep
import json

# function to add to JSON
def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["matches"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

URL = "https://www.opendota.com/matches"
driver = webdriver.Chrome()
driver.get(URL)
sleep(1)
matches = {}
matches_container = driver.find_elements_by_xpath('//*[@id="root"]/div/div[4]/div/div/div/div/div/div/table/tbody')
matches_full = matches_container[0].find_elements_by_xpath('./tr')
print(len(matches_full))
for i, _ in enumerate(matches_full):
    matches_container = driver.find_elements_by_xpath('//*[@id="root"]/div/div[4]/div/div/div/div/div/div/table/tbody')
    match = matches_container[0].find_elements_by_xpath('./tr')[i]
    match.find_elements_by_xpath('./td')[0].find_elements_by_xpath('./div')[0].find_elements_by_xpath('./a')[0].click()

    matches["m"+str(i)] = {}
    sleep(3)
    header = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/header/div[1]')
    header_list = header.text.split('\n')
    print(header_list)
    print(i)
    matches["m"+str(i)]["winning_team"] = header_list[0].replace(' Victory', '')
    matches["m"+str(i)]["kills_radiant"] = header_list[1]
    matches["m"+str(i)]["match_length"] = header_list[3]
    matches["m"+str(i)]["kills_dire"] = header_list[5]
    matches["m"+str(i)]["league"] = header_list[7]
    matches["m"+str(i)]["id"] = header_list[9]
    radiant = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div/div[1]/div[2]/div/div/div/table/tbody')
    if header_list[2] == 'CAPTAINS MODE':
        dire = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div/div[1]/div[5]/div/div/div/table/tbody')
    else:
        dire = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div/div[1]/div[4]/div/div/div/table/tbody')
    players_radiant = radiant.find_elements_by_xpath('./tr')[:5]
    players_dire = dire.find_elements_by_xpath('./tr')[:5]
    players = {}
    for j, player in enumerate(players_radiant+players_dire):
        player_list = player.text.split('\n')
        players["p"+str(j)] = {}
        players["p"+str(j)]["player_name"] = player_list[0]
        players["p"+str(j)]["final_level"] = player_list[2]
        kda = player_list[3].replace('/', '').split(' ')
        players["p"+str(j)]["kda+"] = kda
    matches["m"+str(i)]["players"] = players

    driver.back()
    sleep(2)
print(matches)

