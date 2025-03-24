import os
import telegram
from telegram.ext import Updater, CommandHandler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="👋 Hallo Roman, ich bin dein Wohnungsscout-Bot!")

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
