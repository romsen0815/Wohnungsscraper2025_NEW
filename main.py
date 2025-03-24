import os
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.immo_at import scrape_immo_at
from scrapers.scout24 import scrape_scout24

# Logging konfigurieren
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start-Befehl definieren
async def start(update: Update, context):
    await update.message.reply_text('Hallo! Ich bin dein Immobilien-Bot.')

# Funktion zum Senden von Nachrichten
async def send_telegram_message(bot: Bot, chat_id: int, eintrag: dict):
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

    # Bot und Application initialisieren
    bot = Bot(token=token)
    application = Application.builder().token(token).build()

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

    # Start-Befehl hinzufügen
    application.add_handler(CommandHandler("start", start))

    # Anwendung starten
    await application.initialize()
    await application.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
