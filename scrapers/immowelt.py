import logging
import requests
from requests.exceptions import Timeout

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Funktion zum Abrufen von Daten mit Timeout
def fetch_with_timeout(url):
    try:
        response = requests.get(url, timeout=10)  # 10 Sekunden Timeout
        response.raise_for_status()  # HTTP-Fehler (falls vorhanden) auslösen
        return response.text
    except Timeout:
        logger.error(f"Timeout beim Abrufen der URL: {url}")
        return None
    except requests.RequestException as e:
        logger.error(f"Fehler beim Abrufen der URL: {url}, Fehler: {e}")
        return None

# Deine Scraping-Funktion für Immowelt
def scrape_immowelt():
    logger.debug("Starte Scraping für Immowelt...")
    url = "https://www.immowelt.de/liste/berlin/haeuser/kaufen"
    response = fetch_with_timeout(url)
    if response:
        logger.debug("Erfolgreich Daten von Immowelt abgerufen")
        # Verarbeite die Antwort hier
    else:
        logger.error("Fehler beim Abrufen von Daten von Immowelt")
    # Beispiel-Daten
    daten = [
        {"plattform": "Immowelt", "link": "https://www.immowelt.de/liste/berlin/haeuser/kaufen", "titel": "Beispiel-Inserat"}
    ]
    return daten
