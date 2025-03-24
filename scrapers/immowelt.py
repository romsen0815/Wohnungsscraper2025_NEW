import requests
from bs4 import BeautifulSoup

def scrape_immowelt():
    url = "https://www.immowelt.at/liste/wien/mietwohnungen"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for listing in soup.select(".EstateItem-1f8rnpw"):
        try:
            title = listing.get_text(strip=True)
            link = listing.find("a", href=True)["href"]
            full_link = "https://www.immowelt.at" + link
            results.append({"Titel": title, "Link": full_link})
        except Exception as e:
            print("Fehler:", e)
    return results
