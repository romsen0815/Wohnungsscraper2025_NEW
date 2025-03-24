import os
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.immo_at import scrape_immo_at
from scrapers.scout24 import scrape_scout24
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

def send_telegram_message(entry):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = Bot(token=bot_token)

    text = (
        f"🏠 <b>{entry['titel']}</b>\n"
        f"📍 {entry['ort']}\n"
        f"💰 {entry['preis']}\n"
        f"🌐 Plattform: {entry['plattform']}\n"
        f"🔗 <a href='{entry['link']}'>Zum Inserat</a>"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Anfrage senden", callback_data="anfrage"),
         InlineKeyboardButton("❌ Ignorieren", callback_data="ignorieren")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode="HTML")

def remove_duplicates(entries):
    seen = set()
    unique = []
    for e in entries:
        if e['link'] not in seen:
            seen.add(e['link'])
            unique.append(e)
    return unique

def main():
    print("🔍 Starte Scraper für alle Plattformen...")
    daten = []
    daten += scrape_willhaben()
    daten += scrape_immowelt()
    daten += scrape_immo_at()
    daten += scrape_scout24()

    unique = remove_duplicates(daten)
    print(f"📦 {len(unique)} einzigartige Inserate gefunden")

    for eintrag in unique:
        print(f"Sende: {eintrag['titel']} – {eintrag['plattform']}")
        send_telegram_message(eintrag)

if __name__ == "__main__":
    main()
