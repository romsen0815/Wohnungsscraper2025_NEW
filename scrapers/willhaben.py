import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_willhaben():
    url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/wien"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    listings = soup.select("div[data-cy='search.resultlist.entry']")

    for item in listings:
        try:
            title_tag = item.select_one("h3")
            title = title_tag.text.strip() if title_tag else "Keine Angabe"

            link_tag = item.find("a", href=True)
            link = "https://www.willhaben.at" + link_tag["href"] if link_tag else ""

            ort_tag = item.select_one("div[itemprop='address']")
            ort = ort_tag.text.strip() if ort_tag else "Keine Angabe"

            preis_tag = item.select_one("div[data-cy='search.resultlist.entry.price']")
            preis = preis_tag.text.strip() if preis_tag else "Keine Angabe"

            details = item.select("li")
            flaeche = "Keine Angabe"
            zimmer = "Keine Angabe"
            for d in details:
                txt = d.text.strip()
                if "m²" in txt and flaeche == "Keine Angabe":
                    flaeche = txt.replace("m²", "").strip()
                elif "Zimmer" in txt and zimmer == "Keine Angabe":
                    zimmer = txt.replace("Zimmer", "").strip()

            results.append({
                "titel": title,
                "ort": ort,
                "preis": preis,
                "qm": flaeche,
                "zimmer": zimmer,
                "link": link,
                "plattform": "Willhaben"
            })
        except Exception as e:
            logger.warning(f"Fehler beim Verarbeiten eines Willhaben-Eintrags: {e}")
            continue

    logger.debug(f"Erfolgreich Daten von Willhaben abgerufen: {len(results)} Einträge")
    return results
