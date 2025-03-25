import logging
import os
import requests
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram-Bot-Tokens und Chat-ID aus Umgebungsvariablen lesen
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Standardkriterien
DEFAULT_CRITERIA = {
    "search_query": "",
    "price_from": 0,
    "price_to": 1000,
    "estate_type": 2,
    "area_id": 1010,
    "min_area": 60,
    "max_area": 200,
    "min_rooms": 3,
    "max_rooms": 5,
    "must_have_keywords": "",
    "must_not_have_keywords": "",
    "max_results": 10
}

# Benutzerdefinierte Kriterien speichern
user_criteria = {}

# Start-Befehl
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Willkommen! Geben Sie Ihre Suchkriterien ein.")

# Nachricht behandeln
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    # Kriterien speichern oder Standardkriterien verwenden
    if text.startswith('/criteria'):
        criteria = text.split()[1:]
        if len(criteria) == 10:  # Überprüfen, ob alle erforderlichen Kriterien angegeben sind
            user_criteria[chat_id] = {
                "search_query": criteria[0],
                "price_from": int(criteria[1]),
                "price_to": int(criteria[2]),
                "estate_type": int(criteria[3]),
                "area_id": int(criteria[4]),
                "min_area": int(criteria[5]),
                "max_area": int(criteria[6]),
                "min_rooms": int(criteria[7]),
                "max_rooms": int(criteria[8]),
                "must_have_keywords": criteria[9],
                "must_not_have_keywords": "",
                "max_results": 10
            }
            update.message.reply_text("Kriterien gespeichert.")
        else:
            update.message.reply_text("Bitte geben Sie alle zehn Kriterien in der folgenden Reihenfolge ein: /criteria [search_query] [price_from] [price_to] [estate_type] [area_id] [min_area] [max_area] [min_rooms] [max_rooms] [must_have_keywords]")
    else:
        criteria = user_criteria.get(chat_id, DEFAULT_CRITERIA)
        results = scrape_willhaben(**criteria)
        if results:
            for result in results:
                message = (
                    f"🏠 *{result['title']}*\n"
                    f"📍 {result['location']}\n"
                    f"💰 {result['price']}\n"
                    f"📏 {result['size']} m²\n"
                    f"🏢 {result['rooms']} Zimmer\n"
                    f"🔗 [Zum Inserat]({result['url']})"
                )
                update.message.reply_text(message, parse_mode='Markdown')
        else:
            update.message.reply_text("Keine Ergebnisse gefunden.")

# Hauptfunktion
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
