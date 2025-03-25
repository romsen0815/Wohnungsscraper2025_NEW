import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_willhaben(search_query="", price_from=0, price_to=1000, estate_type=1, area_id=1010, min_area=60, max_area=200, min_rooms=3, max_rooms=5, must_have_keywords="", must_not_have_keywords="", max_results=10):
    base_url = "https://www.willhaben.at/iad/immobilien/"
    params = {
        "SORT": "0",
        "ISPRIVATE": "1",
        "PRICE_FROM": price_from,
        "PRICE_TO": price_to,
        "PROPERTY_TYPE": estate_type,
        "areaId": area_id,
        "ESTATE_SIZE_FROM": min_area,
        "ESTATE_SIZE_TO": max_area,
        "ROOMS_FROM": min_rooms,
        "ROOMS_TO": max_rooms,
        "KEYWORDS": must_have_keywords,
        "EXCLUDE_KEYWORDS": must_not_have_keywords
    }
    url = base_url + "?" + "&".join(f"{key}={value}" for key, value in params.items())
    logger.debug(f"Search URL: {url}")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []

    for entry in soup.select("article[data-ad-id]")[:max_results]:
        try:
            title = entry.select_one("h3").get_text(strip=True)
            price = entry.select_one(".ad-price").get_text(strip=True)
            link = "https://www.willhaben.at" + entry.select_one("a")["href"]
            ort = entry.select_one(".ad-address").get_text(strip=True) if entry.select_one(".ad-address") else "Keine Angabe"

            listings.append({
                "plattform": "Willhaben",
                "titel": title,
                "preis": price,
                "ort": ort,
                "link": link,
                "qm": "Keine Angabe",
                "zimmer": "Keine Angabe"
            })
        except Exception as e:
            logger.warning(f"Fehler beim Parsen eines Eintrags: {e}")
    logger.debug(f"Scraped {len(listings)} listings from Willhaben")
    return listings
