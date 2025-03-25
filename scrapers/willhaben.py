import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_willhaben(search_query, price_from, price_to, estate_type, area_id, min_area, max_area, min_rooms, max_rooms, must_have_keywords, must_not_have_keywords, max_results):
    base_url = "https://www.willhaben.at/iad/immobilien/"

    # Erstelle die Such-URL mit den Filterkriterien
    search_url = f"{base_url}?SORT=0&ISPRIVATE=1&PRICE_FROM={price_from}&PRICE_TO={price_to}&PROPERTY_TYPE={estate_type}&areaId={area_id}&ESTATE_SIZE_FROM={min_area}&ESTATE_SIZE_TO={max_area}&ROOMS_FROM={min_rooms}&ROOMS_TO={max_rooms}&KEYWORDS={search_query}&EXCLUDE_KEYWORDS={must_not_have_keywords}"

    logger.debug("Search URL: %s", search_url)

    response = requests.get(search_url)
    if response.status_code != 200:
        logger.error(f"Fehler beim Abrufen der URL: {search_url}, Statuscode: {response.status_code}")
        return []
        
    soup = BeautifulSoup(response.content, "html.parser")

    listings = []

    for item in soup.find_all('div', class_='search-result-entry', limit=max_results):
        title = item.find('h2', class_='header').get_text(strip=True)
        url = item.find('a', class_='link')['href']
        price = item.find('div', class_='price').get_text(strip=True)
        location = item.find('div', class_='location').get_text(strip=True)
        size = item.find('div', class_='size').get_text(strip=True)
        rooms = item.find('div', class_='rooms').get_text(strip=True)
        
        listings.append({
            'title': title,
            'url': f"https://www.willhaben.at{url}",
            'price': price,
            'location': location,
            'size': size,
            'rooms': rooms
        })

    logger.debug("Scraped %d listings from Willhaben", len(listings))
    return listings
