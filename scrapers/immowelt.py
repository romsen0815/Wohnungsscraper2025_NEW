import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_immowelt():
    url = 'https://www.immowelt.de/suche/berlin/haeuser/kaufen'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for item in soup.find_all('div', class_='search-result-entry'):
        title = item.find('h2', class_='result-list-entry__brand-title').text.strip()
        location = item.find('div', class_='result-list-entry__address').text.strip()
        price = item.find('div', class_='result-list-entry__criteria').text.strip()
        size = item.find('div', class_='result-list-entry__criteria--area').text.strip()
        rooms = item.find('div', class_='result-list-entry__criteria--rooms').text.strip()
        link = item.find('a', class_='result-list-entry__brand-title-container')['href']
        
        results.append({
            'title': title,
            'location': location,
            'price': price,
            'size': size,
            'rooms': rooms,
            'link': link,
            'plattform': 'Immowelt'
        })
    
    logger.debug(f"Erfolgreich Daten von Immowelt abgerufen: {len(results)} Einträge")
    return results
