import json

matches = []

def create_json(new_data, filename='testdata.json'):
    with open(filename,'w+') as file:
        json.dump(new_data, file, indent = 4)

def write_json(new_data, filename='testdata.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside matches
        matches = []
        [matches.append(x) for x in file_data["matches"] if x not in matches]
        matchdict = {'matches':matches}
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(matchdict, file, indent = 4)


match1 =  {'winning_team': 'Team Spirit', 'kills_radiant': '37', 'match_length': '31:18', 'kills_dire': '9', 'league': 'ESL One Fall 2021 powered by Intel', 'match_id': '6148949678' }
matches.append(match1)
matchdict = {'matches':matches}


create_json(matchdict)

write_json(match1)
