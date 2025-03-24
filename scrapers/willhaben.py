import requests
from bs4 import BeautifulSoup

def scrape_willhaben():
    url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?areaId=900&page=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    ads = soup.find_all("div", class_="search-result-entry")
    
    for ad in ads:
        try:
            title = ad.find("div", class_="search-result-entry__header").get_text(strip=True)
            price = ad.find("div", class_="search-result-entry__price").get_text(strip=True)
            location = ad.find("div", class_="search-result-entry__subtitle").get_text(strip=True)
            link = "https://www.willhaben.at" + ad.find("a", href=True)["href"]
            results.append({
                "Titel": title,
                "Preis": price,
                "Ort": location,
                "Link": link
            })
        except Exception as e:
            print("Fehler beim Verarbeiten eines Eintrags:", e)
    return results
