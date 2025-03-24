import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from main import scrape_and_filter  # Importiere die Funktion aus main.py

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Globale Filterkriterien
filter_criteria = {
    "search_query": "Wien Wohnung mieten",
    "price_from": "",
    "price_to": "",
    "estate_type": "",
    "area_id": "",
    "min_area": "",
    "max_area": "",
    "min_rooms": "",
    "max_rooms": "",
    "must_have_keywords": "",
    "must_not_have_keywords": "",
    "max_results": 15
}

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="👋 Hallo Roman, ich bin dein Wohnungsscout-Bot! Verwende /setfilter <query> <price_from> <price_to> <estate_type> <area_id> <min_area> <max_area> <min_rooms> <max_rooms> <must_have_keywords> <must_not_have_keywords> <max_results> um die Suchkriterien zu setzen. Beispiel: /setfilter \"Wien Wohnung mieten\" 500 1500 \"Wohnung\" \"1010\" 50 150 2 4 \"Balkon,Garage\" \"Erdgeschoss\" 10")

def set_filter(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 10:
        update.message.reply_text('Bitte verwende: /setfilter <query> <price_from> <price_to> <estate_type> <area_id> <min_area> <max_area> <min_rooms> <max_rooms> <must_have_keywords> <must_not_have_keywords> [max_results]')
        return

    global filter_criteria
    filter_criteria = {
        "search_query": context.args[0],
        "price_from": context.args[1],
        "price_to": context.args[2],
        "estate_type": context.args[3],
        "area_id": context.args[4],
        "min_area": context.args[5],
        "max_area": context.args[6],
        "min_rooms": context.args[7],
        "max_rooms": context.args[8],
        "must_have_keywords": context.args[9],
        "must_not_have_keywords": context.args[10],
        "max_results": int(context.args[11]) if len(context.args) > 11 else 15
    }

    with open('config.json', 'w') as file:
        json.dump(filter_criteria, file)

    update.message.reply_text('Suchkriterien wurden aktualisiert und gespeichert!')

def scrape_and_send(update: Update, context: CallbackContext) -> None:
    inserate = scrape_and_filter()  # Scraping-Funktion aus main.py
    for eintrag in inserate:
        send_telegram_message(context.bot, CHAT_ID, eintrag)

def send_telegram_message(bot, chat_id, eintrag):
    try:
        link = eintrag.get('link', '')
        if not link.startswith('http'):
            link = 'https://' + link

        text = (
            f"🏠 *{eintrag['titel']}*\n"
            f"📍 {eintrag['ort']}\n"
            f"💰 {eintrag['preis']}\n"
            f"📏 {eintrag.get('qm', 'Keine Angabe')} m²\n"
            f"🛏️ {eintrag.get('zimmer', 'Keine Angabe')} Zimmer\n"
            f"🔗 [Zum Inserat]({link})\n"
            f"🟢 Plattform: {eintrag['plattform']}"
        )

        buttons = [
            [
                InlineKeyboardButton("✅ Anfrage senden", callback_data="anfrage"),
                InlineKeyboardButton("✏️ Nachricht bearbeiten", callback_data="bearbeiten"),
                InlineKeyboardButton("❌ Ignorieren", callback_data="ignorieren"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"⚠️ Fehler beim Senden der Telegram-Nachricht: {e}")

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("setfilter", set_filter))
    dispatcher.add_handler(CommandHandler("scrape_and_send", scrape_and_send))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
