import json
import os

returnList = []
data = open('bookkeeping.json').read()
json_dict = json.loads(data)
#now json_dict is a dictionary
# ex: json_data['64/143']

#There 75 directories and 500 files in each directory
for key, url in json_dict.items():
    filename, file_extension = os.path.splitext(url)
    if file_extension == '.html':
        returnList.append(key)
