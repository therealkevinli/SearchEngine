import json

data = open('./bookkeeping.json').read()
json_dict = json.loads(data)
#now json_dict is a dictionary
# ex: json_data['64/143']
