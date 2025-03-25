import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_willhaben(search_query="", price_from=0, price_to=1000, estate_type=2, area_id=1010, min_area=60, max_area=200, min_rooms=3, max_rooms=5, must_have_keywords="", must_not_have_keywords="", max_results=10):
    url = "https://www.willhaben.at/iad/immobilien/"

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

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    listings = soup.select("div[class^='Box-sc'] a[href*='/iad/immobilien/']")  # Aktualisierter Selektor

    for item in listings:
        try:
            title_tag = item.select_one("h3")
            title = title_tag.text.strip() if title_tag else "Keine Angabe"

            link_tag = item.find("a", href=True)
            link = "https://www.willhaben.at" + link_tag["href"] if link_tag else ""

            ort_tag = item.select_one("div[itemprop='address']")
            ort = ort_tag.text.strip() if ort_tag else "Keine Angabe"

            preis_tag = item.select_one("div[data-cy='resultlist-entry-price']")
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
