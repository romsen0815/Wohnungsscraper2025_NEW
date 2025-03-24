import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import asyncio

from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.immo_at import scrape_immo_at
from scrapers.scout24 import scrape_scout24

async def send_telegram_message(bot, chat_id, eintrag):
    try:
        text = (
            f"🏠 *{eintrag['titel']}*\n"
            f"📍 {eintrag['ort']}\n"
            f"💰 {eintrag['preis']}\n"
            f"🔗 [Zum Inserat]({eintrag['link']})\n"
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

        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"⚠️ Fehler beim Senden der Telegram-Nachricht: {e}")

def remove_duplicates(entries):
    seen = set()
    unique = []
    for e in entries:
        if e.get('link') and e['link'] not in seen:
            seen.add(e['link'])
            unique.append(e)
    return unique

async def main():
    print("🔍 Starte Scraper für alle Plattformen...")
    try:
        daten = []
        daten += scrape_willhaben()
        daten += scrape_immowelt()
        daten += scrape_immo_at()
        daten += scrape_scout24()

        unique = remove_duplicates(daten)
        print(f"📦 {len(unique)} einzigartige Inserate gefunden")

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not token or not chat_id:
            print("❌ Bot-Token oder Chat-ID fehlen.")
            return

        bot = telegram.Bot(token=token)

        for eintrag in unique:
            print(f"📤 Sende: {eintrag['titel']} – {eintrag['plattform']}")
            await send_telegram_message(bot, chat_id, eintrag)

    except Exception as err:
        print(f"🚨 Allgemeiner Fehler: {err}")

if __name__ == "__main__":
    asyncio.run(main())
