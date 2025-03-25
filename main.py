import logging
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.scout24 import scrape_scout24

# Konfiguration Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CRITERIA = {
    "search_query": "Wien Wohnung mieten",
    "price_from": 0,
    "price_to": 1000,
    "estate_type": 2,
    "area_id": 1010,
    "min_area": 60,
    "max_area": 200,
    "min_rooms": 3,
    "max_rooms": 5,
    "must_have_keywords": "",
    "must_not_have_keywords": "",
    "max_results": 10
}

def scrape_and_filter():
    all_data = []

    logger.info("Starte Scraper für alle Plattformen...")

    try:
        data = scrape_willhaben(**DEFAULT_CRITERIA)
        logger.info(f"Daten von Willhaben: {len(data)} Einträge")
        all_data += data
    except Exception as e:
        logger.error(f"Fehler bei Willhaben: {e}")

    try:
        data = scrape_immowelt()
        logger.info(f"Daten von Immowelt: {len(data)} Einträge")
        all_data += data
    except Exception as e:
        logger.error(f"Fehler bei Immowelt: {e}")

    try:
        data = scrape_scout24()
        logger.info(f"Daten von Scout24: {len(data)} Einträge")
        all_data += data
    except Exception as e:
        logger.error(f"Fehler bei Scout24: {e}")

    # Duplikate nach Link entfernen
    seen = set()
    unique = []
    for entry in all_data:
        if entry["link"] not in seen:
            unique.append(entry)
            seen.add(entry["link"])

    logger.info(f"Einzigartige Inserate gefunden: {len(unique)}")
    return unique

if __name__ == "__main__":
    daten = scrape_and_filter()
    for eintrag in daten:
        print(eintrag)
````

Jetzt können wir den nächsten Schritt machen und die anderen Dateien überprüfen.
