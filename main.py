import logging
import os
import requests
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram-Bot-Tokens und Chat-ID aus Umgebungsvariablen lesen
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Funktion zum Senden von Telegram-Nachrichten mit Inline-Keyboard
def send_telegram_message(token, chat_id, message, inline_keyboard):
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'reply_markup': {'inline_keyboard': inline_keyboard}
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logger.info(f"Nachricht erfolgreich gesendet: {message}")
        else:
            logger.error(f"Fehler beim Senden der Nachricht: {response.text}")
    except Exception as e:
        logger.error(f"Exception beim Senden der Nachricht: {e}")

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
    logger.info("Starte Scraper für alle Plattformen...")
    daten = []
    daten += scrape_willhaben()
    logger.info("Daten von Willhaben: %d Einträge", len(daten))
    daten += scrape_immowelt()
    logger.info("Daten von Immowelt: %d Einträge", len(daten))
    # daten += scrape_scout24()  # Vorübergehend auskommentiert

    unique = remove_duplicates(daten)
    logger.info("Einzigartige Inserate gefunden: %d", len(unique))
    
    # Nachrichten mit detaillierten Informationen und Inline-Keyboard erstellen
    for entry in unique:
        message = (
            f"🏠 *{entry.get('title')}*\n"
            f"📍 {entry.get('location')}\n"
            f"💰 {entry.get('price')}\n"
            f"📏 {entry.get('size')} m²\n"
            f"🛏️ {entry.get('rooms')} Zimmer\n"
            f"🔗 [Zum Inserat]({entry.get('link')})\n"
            f"🟢 Plattform: {entry.get('plattform')}"
        )
        
        inline_keyboard = [
            [{'text': '✅ Anfrage senden', 'callback_data': 'anfrage_senden'}],
            [{'text': '✏️ Nachricht bearbeiten', 'callback_data': 'nachricht_bearbeiten'}],
            [{'text': '❌ Ignorieren', 'callback_data': 'ignorieren'}]
        ]
        
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message, inline_keyboard)
    
    return unique

if __name__ == "__main__":
    scrape_and_filter()
