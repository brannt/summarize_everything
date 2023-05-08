import logging
import os
import sys
import traceback

import dotenv
from telegram import Update

dotenv.load_dotenv()


from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from summarizer.core import extract_and_summarize

logger = logging.getLogger(__name__)


TOKEN = os.getenv("SUMMARIZER_TELEGRAM_BOT_TOKEN")
DEBUG = os.environ.get('BOT_DEBUG', False)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi! I'm a summarizer bot. Send me a message and I'll summarize it for you."
    )

def get_updater():
    """Get the updater for the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, summarize))
    return updater

def summarize(update, context):
    """Summarize the message sent to the bot."""
    update.message.reply_text("Summarizing...")
    message_text = update.message.text
    try:
        summary = extract_and_summarize(message_text)
    except Exception as e:
        # Handle the error
        error_message = "There was an error processing your request."
        if DEBUG:
            error_message += "\n\n" + traceback.format_exc()
        
        update.message.reply_text(error_message)
    update.message.reply_text(summary)

def webhook(request, dispatcher):
    """Handle webhook requests from Telegram"""
    update = Update.de_json(request.get_json(force=True), dispatcher.bot)
    dispatcher.process_update(update)
    return "ok"

def start_polling():
    """Start the bot."""
    updater = get_updater()
    logger.info("Starting bot")
    updater.start_polling()
    updater.idle()

def start_webhook(url, host, port):
    """Start the bot."""
    updater = get_updater()
    logger.info("Starting bot")
    updater.start_webhook(listen=host, port=port, url_path=TOKEN, webhook_url=f"{url}/{TOKEN}")

def set_webhook(url):
    """Set the webhook for the bot."""
    updater = Updater(TOKEN, use_context=True)
    updater.bot.set_webhook(f"{url}/{TOKEN}")

def delete_webhook():
    """Delete the webhook for the bot."""
    updater = Updater(TOKEN, use_context=True)
    updater.bot.delete_webhook()

def guard_exit(condition, message):
    """Exit with an error message if the condition is true."""
    if condition:
        print(message)
        sys.exit(1)

def main():
    """Run the bot."""
    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s %(message)s", level=logging.INFO
    )
    guard_exit(len(sys.argv) < 2, "Usage: python -m summarizer.integrations.telegram <command>")
    command = sys.argv[1]
    if command == "start-polling":
        start_polling()
    elif command == "start-webhook":
        guard_exit(len(sys.argv) < 3, "Usage: python -m summarizer.integrations.telegram start-webhook <host:port>")
        url = sys.argv[2]
        if len(sys.argv) > 3:
            host, port = sys.argv[3].split(":")
        else:
            host, port = "127.0.0.1", 8000
        start_webhook(url, host, port)
    elif command == "set-webhook":
        guard_exit(len(sys.argv) < 3, "Usage: python -m summarizer.integrations.telegram set-webhook <url>")
        url = sys.argv[2]
        set_webhook(url)
    elif command == "delete-webhook":
        delete_webhook()
    else:
        guard_exit(True, f"Unknown command: {command}")

if __name__ == "__main__":
    main()
