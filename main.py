from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.immo_at import scrape_immo_at
from scrapers.scout24 import scrape_scout24

def main():
    print("🔍 Starte Scraper für alle Plattformen...")
    daten = []
    daten += scrape_willhaben()
    daten += scrape_immowelt()
    daten += scrape_immo_at()
    daten += scrape_scout24()

    # Duplikate nach Link entfernen
    unique = []
    seen = set()
    for eintrag in daten:
        link = eintrag.get("Link")
        if link and link not in seen:
            seen.add(link)
            unique.append(eintrag)

    for eintrag in unique:
        print(eintrag)

if __name__ == "__main__":
    main()
