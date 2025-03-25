import json
import logging
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt

# Konfiguriere das Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Definiere die Filterkriterien für den Test
filter_criteria = {
    "search_query": "wohnung",
    "price_from": "500",
    "price_to": "1500",
    "estate_type": "apartment",
    "area_id": "12345",
    "min_area": "50",
    "max_area": "100",
    "min_rooms": "2",
    "max_rooms": "4",
    "must_have_keywords": "",
    "must_not_have_keywords": "",
    "max_results": 10
}

def test_scrape_platforms():
    logger.debug("Start scraping test with filter criteria: %s", filter_criteria)
    
    # Scrape Willhaben
    willhaben_inserate = scrape_willhaben(
        filter_criteria['search_query'],
        filter_criteria['price_from'],
        filter_criteria['price_to'],
        filter_criteria['estate_type'],
        filter_criteria['area_id'],
        filter_criteria['min_area'],
        filter_criteria['max_area'],
        filter_criteria['min_rooms'],
        filter_criteria['max_rooms'],
        filter_criteria['must_have_keywords'],
        filter_criteria['must_not_have_keywords'],
        filter_criteria['max_results']
    )
    logger.debug("Scraping Willhaben completed, found %d listings", len(willhaben_inserate))

    for eintrag in willhaben_inserate:
        logger.debug("Willhaben Listing: %s", json.dumps(eintrag, indent=2, ensure_ascii=False))
        print(f"Willhaben Inserat: {eintrag['title']} - {eintrag['url']}")
    
    # Scrape Immowelt
    immowelt_inserate = scrape_immowelt(filter_criteria['search_query'])
    logger.debug("Scraping Immowelt completed, found %d listings", len(immowelt_inserate))

    for eintrag in immowelt_inserate:
        logger.debug("Immowelt Listing: %s", json.dumps(eintrag, indent=2, ensure_ascii=False))
        print(f"Immowelt Inserat: {eintrag['title']} - {eintrag['url']}")

if __name__ == "__main__":
    test_scrape_platforms()
