import os
import json
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import nest_asyncio
from main import scrape_and_filter  # Importiere die Funktion aus main.py

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Überprüfe, ob die Umgebungsvariablen gesetzt sind
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    logger.error("TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID müssen gesetzt sein.")
    exit(1)

# Der restliche Code bleibt unverändert

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Start command received")
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="👋 Hallo! Ich bin dein Wohnungsscout-Bot! Verwende /setfilter, um die Suchkriterien zu setzen.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Help command received")
    help_text = """
    Hier sind die verfügbaren Befehle:
    /start - Bot starten
    /help - Diese Hilfe anzeigen
    /setfilter - Setze Filterkriterien (z.B. /setfilter min_qm=50 max_price=1500)
    """
    await update.message.reply_text(help_text)

async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Set filter command received with args: %s", context.args)
    if len(context.args) < 10:
        await update.message.reply_text('Bitte verwende: /setfilter <query> <price_from> <price_to> <estate_type> <area_id> <min_area> <max_area> <min_rooms> <max_rooms> <must_have_keywords> <must_not_have_keywords> [max_results]')
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
        logger.debug("Suchkriterien in config.json gespeichert: %s", filter_criteria)

    await update.message.reply_text('Suchkriterien wurden aktualisiert und gespeichert!')

async def scrape_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Scrape and send command received")
    inserate = scrape_and_filter()  # Scraping-Funktion aus main.py
    logger.debug("Scraping completed, found %d listings", len(inserate))
    for eintrag in inserate:
        logger.debug(f"Sending listing: {eintrag}")
        await send_telegram_message(context.bot, TELEGRAM_CHAT_ID, eintrag)

async def send_telegram_message(bot, chat_id, eintrag):
    try:
        link = eintrag.get('link', '')
        if not link.startswith('http'):
            link = 'https://' + link

        text = (
            f"🏠 *{eintrag['titel']}*\n"
            f"📍 {eintrag['ort']}\n"
            f"💰 {eintrag['preis']}*\n"
            f"📏 {eintrag.get('qm', 'Keine Angabe')} m²*\n"
            f"🛏️ {eintrag.get('zimmer', 'Keine Angabe')} Zimmer*\n"
            f"🔗 [Zum Inserat]({link})\n"
            f"🟢 Plattform: {eintrag['plattform']}*"
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
            parse_mode='Markdown',
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        logger.debug("Nachricht gesendet: %s", text)
    except Exception as e:
        logger.error("Fehler beim Senden der Telegram-Nachricht: %s", e)

async def main() -> None:
    logger.debug("Bot startet")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setfilter", set_filter))
    application.add_handler(CommandHandler("scrape_and_send", scrape_and_send))

    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.debug("Application cancelled")
    finally:
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
