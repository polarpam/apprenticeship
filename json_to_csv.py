import json
import csv

input_file = 'vacancies_transformed.json'
output_file = 'vacancies_list.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

if data and isinstance(data, list) and isinstance(data[0], dict):
    headers = list(data[0].keys())
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data successfully written to {output_file}")
else:
    print("JSON data is empty or not in the expected format.")
