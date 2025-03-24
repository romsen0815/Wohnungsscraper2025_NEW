import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="👋 Hallo Roman, ich bin dein Wohnungsscout-Bot! Verwende /set <query> <price_from> <price_to> <estate_type> <area_id> <min_area> <max_area> <min_rooms> <max_rooms> <must_have_keywords> <must_not_have_keywords> <max_results> um die Suchkriterien zu setzen.")

def set_criteria(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 10:
        update.message.reply_text('Bitte verwende: /set <query> <price_from> <price_to> <estate_type> <area_id> <min_area> <max_area> <min_rooms> <max_rooms> <must_have_keywords> <must_not_have_keywords> [max_results]')
        return

    config = {
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
        json.dump(config, file)

    update.message.reply_text('Suchkriterien wurden aktualisiert!')

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set", set_criteria))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()# Telegram-Bot Integration erfolgt hier.
