import json

with open('urls.json', 'r') as file:
    data = json.load(file)

sorted_data = dict(sorted(data.items()))

with open('urls.json', 'w') as file:
    json.dump(sorted_data, file, indent=4)
