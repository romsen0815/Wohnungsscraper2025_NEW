(venv) rmansenkl@rmans-MacBook-Pro-3 Wohnungsscraper2025_NEW % python main.py
INFO:__main__:Starte Scraper für alle Plattformen...
DEBUG:scrapers.willhaben:Search URL: https://www.willhaben.at/iad/immobilien/?SORT=0&ISPRIVATE=1&PRICE_FROM=0&PRICE_TO=1000&PROPERTY_TYPE=2&areaId=1010&ESTATE_SIZE_FROM=60&ESTATE_SIZE_TO=200&ROOMS_FROM=3&ROOMS_TO=5&KEYWORDS=&EXCLUDE_KEYWORDS=
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): www.willhaben.at:443
DEBUG:urllib3.connectionpool:https://www.willhaben.at:443 "GET /iad/immobilien/?SORT=0&ISPRIVATE=1&PRICE_FROM=0&PRICE_TO=1000&PROPERTY_TYPE=2&areaId=1010&ESTATE_SIZE_FROM=60&ESTATE_SIZE_TO=200&ROOMS_FROM=3&ROOMS_TO=5&KEYWORDS=&EXCLUDE_KEYWORDS= HTTP/1.1" 200 None
DEBUG:scrapers.willhaben:Scraped 0 listings from Willhaben
INFO:__main__:Daten von Willhaben: 0 Einträge
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): www.immowelt.de:443
DEBUG:urllib3.connectionpool:https://www.immowelt.de:443 "GET /suche/wien/wohnung/mieten HTTP/1.1" 404 None
DEBUG:scrapers.immowelt:Erfolgreich Daten von Immowelt abgerufen: 0 Einträge
INFO:__main__:Daten von Immowelt: 0 Einträge
DEBUG:scrapers.scout24:Starte Scraping für Scout24...
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): www.scout24.de:44
ChatGPT said:

Danke für dein Log – das zeigt uns genau, wo’s hakt. Hier ist die präzise Analyse deines aktuellen Scraper-Status für die drei Plattformen:
✅ 1. Willhaben

    Die URL wird korrekt gebaut (mit den richtigen Parametern).

    Der HTTP-Status ist 200, also erfolgreich.

    Aber: Scraped 0 listings → bedeutet, dass das HTML korrekt geladen wurde, aber keine Inserate extrahiert werden konnten.

🔍 Vermutung:

    Die HTML-Struktur von Willhaben hat sich geändert.

    Dein Scraper sucht vermutlich nach veralteten CSS-Klassen wie div.ad-container o. ä., die nicht mehr existieren.

    Willhaben verwendet mittlerweile starkes JavaScript-Rendering, wodurch Listings erst clientseitig nachgeladen werden.

❌ 2. Immowelt

    Deine URL: https://www.immowelt.de/suche/wien/wohnung/mieten

    Antwort: 404 Not Found

    Scraper meldet trotzdem „Erfolgreich“ – obwohl keine Einträge!

🔍 Fehler:

    Die URL ist falsch – der korrekte Pfad für Wien bei Immowelt ist:

    https://www.immowelt.at/liste/wien/wohnungen/mieten

    Außerdem scrapest du .de statt .at → für Wien brauchst du unbedingt immowelt.at, nicht immowelt.de!

⚠️ 3. Scout24

    Hier bricht der Log ab, aber der Hostname www.scout24.de ist nicht mehr gültig für Immobiliensuche.

    Du brauchst immobilienscout24.de (Deutschland) oder immobilienscout24.at (Österreich).

    Auch hier ist das HTML dynamisch und muss exakt analysiert werden, sonst bekommst du kein Ergebnis.

✅ Nächste Schritte (empfohlen):

    Willhaben-Scraper anpassen: Mit BeautifulSoup auf aktuelle HTML-Struktur prüfen, oder auf Selenium / Playwright umstellen.

    Immowelt auf .at umstellen – URL ändern zu:

https://www.immowelt.at/liste/wien/wohnungen/mieten

und Scraper an neue Seite anpassen.

Scout24 URL + Struktur anpassen (aktuell ohne Wirkung).
