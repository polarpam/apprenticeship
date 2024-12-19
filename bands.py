import json
import re
from collections import Counter

with open('vacancies_transformed.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

level_pattern = re.compile(r'level (\d+)', re.IGNORECASE)
target_level = 'level 2'

bands = [
    (5000, 8999), 
    (9000, 12999), 
    (13000, 16999), 
    (17000, 20999), 
    (21000, 24999), 
    (25000, 28999), 
    (29000, 32999), 
    (33000, 36999), 
    (37000, 40999)
]

band_counter = Counter()

for entry in data:
    training_course = entry.get('training_course', '')
    matches = level_pattern.findall(training_course)
    
    if target_level.split()[-1] in matches:
        wage = entry.get('transformed_wage')
        if wage is None or not isinstance(wage, (int, float)):
            continue
        
        for lower, upper in bands:
            if lower <= wage <= upper:
                band_label = f"{lower}-{upper}"
                band_counter[band_label] += 1
                break

sorted_bands = sorted(band_counter.items(), key=lambda x: int(x[0].split('-')[0]))

print(f'Wage Bands for {target_level}:')
for band, count in sorted_bands:
    print(f"{band}: {count}")
