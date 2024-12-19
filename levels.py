import json
import re
from collections import Counter

with open('copy.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

level_counter = Counter()
level_pattern = re.compile(r'level (\d+)', re.IGNORECASE)
no_level_entries = 0

for entry in data:
    training_course = entry.get('training_course', '')
    matches = level_pattern.findall(training_course)
    if not matches:
        no_level_entries += 1
    for match in matches:
        level_counter[f'level {match}'] += 1

print("Level Occurrences:")
for level, count in sorted(level_counter.items()):
    print(f"{level}: {count}")

print(f"\nEntries with no level specified: {no_level_entries}")
print(f"Total entries: {len(data)}")
