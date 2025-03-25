import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_willhaben(search_query, price_from, price_to, estate_type, area_id, min_area, max_area, min_rooms, max_rooms, must_have_keywords, must_not_have_keywords, max_results):
    url = 'https://www.willhaben.at/iad/immobilien/'
    
    params = {
        'SORT': 0,
        'ISPRIVATE': 1,
        'PRICE_FROM': price_from,
        'PRICE_TO': price_to,
        'PROPERTY_TYPE': estate_type,
        'areaId': area_id,
        'ESTATE_SIZE_FROM': min_area,
        'ESTATE_SIZE_TO': max_area,
        'ROOMS_FROM': min_rooms,
        'ROOMS_TO': max_rooms,
        'KEYWORDS': search_query,
        'EXCLUDE_KEYWORDS': must_not_have_keywords,
    }
    
    response = requests.get(url, params=params)
    logger.debug(f"Search URL: {response.url}")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for item in soup.find_all('div', class_='search-result-entry'):
        title = item.find('h2', class_='header').text.strip()
        location = item.find('div', class_='location').text.strip()
        price = item.find('div', class_='price').text.strip()
        size = item.find('div', class_='size').text.strip()
        rooms = item.find('div', class_='rooms').text.strip()
        link = item.find('a', class_='link')['href']
        
        results.append({
            'title': title,
            'location': location,
            'price': price,
            'size': size,
            'rooms': rooms,
            'link': link,
            'plattform': 'Willhaben'
        })
    
    logger.debug(f"Scraped {len(results)} listings from Willhaben")
    return results[:max_results]
