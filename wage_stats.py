import json
import re
from statistics import mean, median, mode, StatisticsError

with open('vacancies_transformed.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

level_pattern = re.compile(r'level (\d+)', re.IGNORECASE)
level_stats = {}

for entry in data:
    training_course = entry.get('training_course', '')
    transformed_wage = entry.get('transformed_wage')
    matches = level_pattern.findall(training_course)
    
    if matches and transformed_wage is not None:
        level = f"level {matches[0]}"
        if level not in level_stats:
            level_stats[level] = {"wages": []}
        level_stats[level]["wages"].append(transformed_wage)

for level, stats in level_stats.items():
    wages = stats["wages"]
    level_stats[level]["mean_wage"] = mean(wages) if wages else 0
    level_stats[level]["median_wage"] = median(wages) if wages else 0
    try:
        level_stats[level]["mode_wage"] = mode(wages) if wages else None
    except StatisticsError:
        level_stats[level]["mode_wage"] = None
    level_stats[level]["highest_wage"] = max(wages) if wages else 0
    level_stats[level]["lowest_wage"] = min(wages) if wages else 0
    del level_stats[level]["wages"]

with open('level_wage_stats_detailed.json', 'w', encoding='utf-8') as outfile:
    json.dump(level_stats, outfile, ensure_ascii=False, indent=2)

print("Wage statistics by level have been calculated and saved to 'level_wage_stats_detailed.json'.")
