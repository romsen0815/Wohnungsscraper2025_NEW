import os
import logging
import requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode
from scrapers.willhaben import scrape_willhaben
from scrapers.immowelt import scrape_immowelt
from scrapers.scout24 import scrape_scout24

# Filterkriterien als globale Variablen
filter_criteria = {
    "min_qm": 40,
    "max_price": 1000,
    "districts": [1020, 1070, 1080, 1050],
    "must_have_keywords": ["Altbau", "Balkon", "Terrasse", "ruhig"],
    "ignore_keywords": ["Untermiete", "befristet", "WG-Zimmer"]
}

# Logging konfigurieren
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram-Bot-Token und Chat-ID aus Umgebungsvariablen
token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Telegram-Bot initialisieren
bot = Bot(token=token)
application = Application.builder().token(token).build()

# Start-Befehl
async def start(update: Update, context):
    await update.message.reply_text('Hallo! Ich bin dein Immobilien-Bot. Verwende /help, um die Befehle zu sehen.')

# Help-Befehl - Listet alle verfügbaren Befehle auf
async def help_command(update: Update, context):
    help_text = """
    Hier sind die verfügbaren Befehle:
    /start - Bot starten
    /help - Diese Hilfe anzeigen
    /setfilter - Setze Filterkriterien (z.B. /setfilter min_qm=50 max_price=1500)
    """
    await update.message.reply_text(help_text)

# Funktion zum Senden von Telegram-Nachrichten
async def send_telegram_message(bot, chat_id, eintrag):
    try:
        link = eintrag.get('link', '')
        if not link.startswith('http'):
            link = 'https://' + link

        text = (
            f"🏠 *{eintrag['titel']}*
"
            f"📍 {eintrag['ort']}
"
            f"💰 {eintrag['preis']}
"
            f"📏 {eintrag.get('qm', 'Keine Angabe')} m²
"
            f"🛏️ {eintrag.get('zimmer', 'Keine Angabe')} Zimmer
"
            f"🔗 [Zum Inserat]({link})
"
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

        # Nachricht senden
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"⚠️ Fehler beim Senden der Telegram-Nachricht: {e}")

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

# Funktion zum Scrapen der Inserate
async def scrape_and_send():
    # Scraping durchführen
    logger.info("🔍 Starte Scraper für alle Plattformen...")
    daten = []
    daten += scrape_willhaben()
    daten += scrape_immowelt()
    daten += scrape_scout24()

    unique = remove_duplicates(daten)
    logger.info(f"📦 {len(unique)} einzigartige Inserate gefunden")

    # Nachrichten senden
    for eintrag in unique:
        logger.info(f"📤 Sende: {eintrag['titel']} – {eintrag['plattform']}")
        await send_telegram_message(bot, chat_id, eintrag)

# Befehl um die Filter zu setzen (über Telegram)
async def set_filter(update: Update, context):
    global filter_criteria

    if len(context.args) < 2:
        await update.message.reply_text("Bitte gib die Filterkriterien im Format 'key=value' an, z.B. /setfilter max_price=1500 min_qm=50")
        return

    # Beispiel: max_price=1500
    for i in range(0, len(context.args), 2):
        key = context.args[i]
        value = context.args[i + 1]

        # Filter aktualisieren
        if key in filter_criteria:
            filter_criteria[key] = value
            await update.message.reply_text(f"Filter '{key}' auf {value} gesetzt.")
        else:
            await update.message.reply_text(f"Unbekannter Filter '{key}'!")

# Telegram-Handler und Start der Anwendung
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("setfilter", set_filter))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, scrape_and_send))

# Start der Telegram-Bot Anwendung
if __name__ == "__main__":
    application.run_polling()
