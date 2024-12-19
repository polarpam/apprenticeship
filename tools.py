import json

with open('copy.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

if isinstance(data, list):
    entry_count = len(data)
    print(f"There are {entry_count} entries in the list.")
else:
    print("The JSON data is not a list. Please check the file format.")


