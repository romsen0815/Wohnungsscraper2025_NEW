import requests
from bs4 import BeautifulSoup

def scrape_willhaben():
    url = "https://www.willhaben.at/iad/immobilien/immobiliensuche"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    inserate = []

    for item in soup.find_all('div', class_='result-item'):  # Beispielhafte Klasse für ein Inserat
        title = item.find('h2', class_='title-class').text.strip()
        price = item.find('span', class_='price-class').text.strip()
        location = item.find('span', class_='location-class').text.strip()
        link = item.find('a', class_='link-class')['href']
        
        inserate.append({
            'plattform': 'Willhaben',
            'titel': title,
            'preis': price,
            'ort': location,
            'link': f"https://www.willhaben.at{link}"
        })

    return inserate
