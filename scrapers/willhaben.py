❌ PROBLEM 1: Willhaben-Scraper – keine Einträge

Fehlerhafte Selektoren + veraltete Klassen

for item in soup.find_all('div', class_='search-result-entry'):

    Diese Klasse existiert nicht mehr auf willhaben.at.

    Auch andere Selektoren wie 'h2.header', 'div.location', 'div.price', usw. sind nicht korrekt.

🔧 Lösung: Die aktuelle Struktur von Willhaben benötigt:

    div mit Attribut data-cy="search.resultlist" als Container

    Innerhalb: div mit data-cy="search.resultlist.entry" (für jeden Eintrag)

Die relevanten Daten (Preis, Größe, Zimmer, Link etc.) müssen aus verschachtelten <a>, <h3>, <span> usw. extrahiert werden – teils auch mit regulären Ausdrücken oder über Attribute.
❌ PROBLEM 2: Immowelt-Scraper – None-Werte

Grund: Die Klassen im HTML stimmen nicht mehr mit dem Code überein:

item.find('h2', class_='result-list-entry__brand-title')  # ❌ existiert nicht mehr

Auch hier sind z. B. die tatsächlichen Strukturen:

    'div[data-test="object-listing"]' für einzelne Einträge

    Innerhalb: andere moderne CSS-Klassen oder data-* Attribute

🔧 Lösung: Selektoren müssen an den aktuellen HTML-Baum angepasst werden. Sonst wird nichts gefunden → deshalb None.
