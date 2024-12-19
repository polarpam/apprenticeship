import json
import re

with open('vacancies.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

wage_pattern = re.compile(r'£([\d,\.]+)')

for entry in data:
    annual_wage = entry.get('annual_wage', '').strip()
    transformed_wage = None

    if annual_wage:
        wage_matches = wage_pattern.findall(annual_wage)
        if wage_matches:
            first_wage = wage_matches[0]
            try:
                cleaned_wage = first_wage.replace(',', '').rstrip('.')
                transformed_wage = float(cleaned_wage)
            except ValueError:
                pass

    entry['transformed_wage'] = transformed_wage

with open('vacancies_transformed.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=2)

print("Updated JSON file with transformed_wage field has been created as 'vacancies_transformed.json'.")
