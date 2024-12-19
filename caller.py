import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://www.findapprenticeship.service.gov.uk"
main_url_template = "https://www.findapprenticeship.service.gov.uk/apprenticeships?sort=DistanceAsc&pageNumber={}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def scrape_vacancy_details(vacancy_url):
    response = requests.get(vacancy_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        vacancy_data = {}
        vacancy_data['url'] = vacancy_url

        title = soup.find('h1', class_='govuk-heading-l faa-vacancy__title')
        vacancy_data['title'] = title.get_text(strip=True) if title else 'N/A'

        organization = soup.find('p', class_='govuk-body-l faa-vacancy__organisation')
        vacancy_data['organization'] = organization.get_text(strip=True) if organization else 'N/A'

        location = soup.find('p', class_='govuk-body-l faa-vacancy__location')
        vacancy_data['location'] = location.get_text(strip=True) if location else 'N/A'

        closing_date = soup.find('p', class_='govuk-body faa-vacancy__closing-date')
        vacancy_data['closing_date'] = closing_date.get_text(strip=True) if closing_date else 'N/A'

        posted_date = soup.find('p', class_='govuk-body govuk-!-font-size-16 das-!-color-dark-grey')
        vacancy_data['posted_date'] = posted_date.get_text(strip=True) if posted_date else 'N/A'

        summary_section = soup.find('dl', class_='govuk-summary-list')
        if summary_section:
            for row in summary_section.find_all('div', class_='govuk-summary-list__row'):
                key = row.find('dt', class_='govuk-summary-list__key')
                value = row.find('dd', class_='govuk-summary-list__value')
                if key and value:
                    field_name = key.get_text(strip=True).lower().replace(' ', '_')
                    field_value = value.get_text(strip=True)
                    vacancy_data[field_name] = field_value

        return vacancy_data
    else:
        print(f"Failed to fetch vacancy page: {vacancy_url}. Status code: {response.status_code}")
        return None

start_time = time.time()
all_vacancies = []

for page_number in range(1, 537):
    main_url = main_url_template.format(page_number)
    print(f"Scraping page {page_number}: {main_url}")
    response = requests.get(main_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        vacancy_links = soup.find_all('a', class_='das-search-results__link')
        print(f"Found {len(vacancy_links)} vacancies on page {page_number}")

        if not vacancy_links:
            print(f"No vacancies found on page {page_number}. Stopping further scraping.")
            break

        for link in vacancy_links:
            href = link['href']
            full_url = f"{base_url}{href}"
            print(f"Scraping vacancy: {full_url}")
            vacancy_details = scrape_vacancy_details(full_url)
            if vacancy_details:
                all_vacancies.append(vacancy_details)
    else:
        print(f"Failed to fetch the main page for page {page_number}. Status code: {response.status_code}")
        break

end_time = time.time()
elapsed_time = (end_time - start_time) / 60

with open('vacancies.json', 'w') as json_file:
    json.dump(all_vacancies, json_file, indent=4)

print(f"Total time taken: {elapsed_time:.2f} minutes.")
