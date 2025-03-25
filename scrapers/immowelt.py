import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_immowelt():
    url = 'https://www.immowelt.de/suche/berlin/haeuser/kaufen'
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    listings = soup.select("div[data-test='object-listing']")

    for item in listings:
        try:
            title_tag = item.select_one("h2")
            title = title_tag.text.strip() if title_tag else "Keine Angabe"

            link_tag = item.find("a", href=True)
            link = link_tag["href"] if link_tag else ""

            ort_tag = item.select_one("div[data-test='address']")
            ort = ort_tag.text.strip() if ort_tag else "Keine Angabe"

            preis_tag = item.select_one("div[data-test='price']")
            preis = preis_tag.text.strip() if preis_tag else "Keine Angabe"

            flaeche = "Keine Angabe"
            zimmer = "Keine Angabe"
            details = item.select("div[data-test='additional-info'] span")
            for d in details:
                txt = d.text.strip()
                if "m²" in txt and flaeche == "Keine Angabe":
                    flaeche = txt
                elif "Zimmer" in txt and zimmer == "Keine Angabe":
                    zimmer = txt

            results.append({
                "titel": title,
                "ort": ort,
                "preis": preis,
                "qm": flaeche,
                "zimmer": zimmer,
                "link": link,
                "plattform": "Immowelt"
            })
        except Exception as e:
            logger.warning(f"Fehler beim Verarbeiten eines Immowelt-Eintrags: {e}")
            continue

    logger.debug(f"Erfolgreich Daten von Immowelt abgerufen: {len(results)} Einträge")
    return results
