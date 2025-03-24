import os
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import asyncio

from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.immo_at import scrape_immo_at
from scrapers.scout24 import scrape_scout24

# Logging konfigurieren
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start-Befehl definieren
async def start(update, context):
    await update.message.reply_text('Hallo! Ich bin dein Immobilien-Bot.')

# Funktion zum Senden von Nachrichten
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
        logger.error(f"⚠️ Fehler beim Senden der Telegram-Nachricht: {e}")

# Funktion zum Entfernen von Duplikaten
def remove_duplicates(entries):
    seen = set()
    unique = []
    for e in entries:
        if e.get('link') and e['link'] not in seen:
            seen.add(e['link'])
            unique.append(e)
    return unique

# Hauptfunktion zum Scrapen und Senden von Nachrichten
async def main():
    # Bot-Token und Chat-ID aus Umgebungsvariablen
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.error("Bot-Token oder Chat-ID fehlen.")
        return

    logger.info(f"🚨 Chat-ID: {chat_id}")  # Chat-ID im Log ausgeben

    # Bot und Application initialisieren
    bot = Bot(token=token)

    # Scraping durchführen
    logger.info("🔍 Starte Scraper für alle Plattformen...")
    daten = []
    daten += scrape_willhaben()
    daten += scrape_immowelt()
    daten += scrape_immo_at()
    daten += scrape_scout24()

    # Duplikate entfernen
    unique = remove_duplicates(daten)
    logger.info(f"📦 {len(unique)} einzigartige Inserate gefunden")

    # Nachrichten senden
    for eintrag in unique:
        logger.info(f"📤 Sende: {eintrag['titel']} – {eintrag['plattform']}")
        await send_telegram_message(bot, chat_id, eintrag)

if __name__ == "__main__":
    asyncio.run(main())
