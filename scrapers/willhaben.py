Hier ist meine vollständige Analyse zu deinen beiden Scraper-Modulen (willhaben.py und immowelt.py):
✅ 1. immowelt.py funktioniert größtenteils korrekt
Positives:

    ✅ Es wird die richtige URL verwendet:
    https://www.immowelt.de/suche/berlin/haeuser/kaufen

    ✅ Es wird ein User-Agent gesetzt – das ist wichtig, damit die Seite nicht blockiert.

    ✅ Die Listings werden mit dem Selektor div[data-test='object-listing'] korrekt extrahiert.

    ✅ Titel, Link, Ort, Preis, Quadratmeter und Zimmeranzahl werden versucht zu extrahieren.

Probleme:

    ⚠️ Die URL ist hartkodiert auf „Haus kaufen in Berlin“, nicht aber deine tatsächlichen Filterkriterien (z. B. Mietwohnung in Wien).

    ⚠️ Die Werte qm, zimmer etc. werden nur gesetzt, wenn die Zeichenfolge "m²" oder "Zimmer" vorkommt, was in manchen Anzeigen nicht exakt so auftaucht → dann bleibt None.

Verbesserungsvorschläge:

    ➕ Parameterisieren der URL (z. B. Wien, Wohnung, Miete).

    ➕ Bessere Fehlerbehandlung, falls select() oder find() nichts ergibt.

    🔍 Logging bei leerem Ergebnis, um Ursachen leichter zu erkennen.

⚠️ 2. willhaben.py funktioniert aktuell nicht – gibt immer 0 Einträge zurück
Hauptursache:

url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/wien"

Diese URL ignoriert alle Filterparameter, weil es sich um eine vorgefilterte URL handelt.

Zudem:

listings = soup.select("div[data-cy='search.resultlist.entry']")

Dieser Selektor ist nicht mehr gültig. Willhaben hat das HTML geändert. Aktuell funktioniert z. B.:

soup.select("div[class^='Box-sc'] a[href*='/iad/immobilien/']")

🛠 Zusammenfassung der Fehlerquellen:
Modul	Problembeschreibung
willhaben.py	❌ Filter-URL inkorrekt
❌ CSS-Selektor findet keine Listings
immowelt.py	⚠️ Feste URL (Berlin, Kaufen)
⚠️ Parser zu sensitiv gegenüber Variationen
main.py	❌ Übergibt Filterparameter an scrape_willhaben(), die dort nicht definiert sind
