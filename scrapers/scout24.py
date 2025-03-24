import requests
from bs4 import BeautifulSoup

def scrape_scout24():
    url = "https://www.scout24.de/immobilien"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    inserate = []

    for item in soup.find_all('div', class_='result-list-entry'):
        title = item.find('a', class_='result-list-entry__brand-title').text.strip()
        price = item.find('div', class_='result-list-entry__price').text.strip()
        location = item.find('div', class_='result-list-entry__location').text.strip()
        link = item.find('a', class_='result-list-entry__brand-title')['href']
        
        inserate.append({
            'plattform': 'Scout24',
            'titel': title,
            'preis': price,
            'ort': location,
            'link': f"https://www.scout24.de{link}"
        })

    return inserate
