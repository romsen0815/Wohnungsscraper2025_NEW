import os
import logging
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.scout24 import scrape_scout24

# Filterkriterien als globale Variablen
filter_criteria = {
    "min_qm": 40,
    "max_price": 1000,
    "districts": [1020, 1070, 1080, 1050],
    "must_have_keywords": ["Altbau", "Balkon", "Terrasse", "ruhig"],
    "ignore_keywords": ["Untermiete", "befristet", "WG-Zimmer"]
}

# Duplikate basierend auf Link und Plattform filtern
def remove_duplicates(entries):
    seen = set()
    unique = []
    for e in entries:
        identifier = (e.get('link'), e.get('plattform'))
        if identifier not in seen:
            seen.add(identifier)
            unique.append(e)
    return unique

# Scraping durchführen und Ergebnisse filtern
def scrape_and_filter():
    print("🔍 Starte Scraper für alle Plattformen...")
    daten = []
    daten += scrape_willhaben()
    daten += scrape_immowelt()
    daten += scrape_scout24()

    unique = remove_duplicates(daten)
    print(f"📦 {len(unique)} einzigartige Inserate gefunden")

    # Ergebnisse zurückgeben
    return unique
