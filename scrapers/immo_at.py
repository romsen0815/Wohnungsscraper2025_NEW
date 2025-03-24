import requests
from bs4 import BeautifulSoup

def scrape_immo_at():
    url = "https://www.immo.at/mieten/wohnung/wien"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for listing in soup.find_all("div", class_="result-item"):
        try:
            title = listing.get_text(strip=True)
            link = listing.find("a", href=True)["href"]
            full_link = "https://www.immo.at" + link
            results.append({"Titel": title, "Link": full_link})
        except Exception as e:
            print("Fehler:", e)
    return results
