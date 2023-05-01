import logging
import os

import dotenv

dotenv.load_dotenv()


from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from summarizer.core import extract_and_summarize

logger = logging.getLogger(__name__)


TOKEN = os.getenv("SUMMARIZER_TELEGRAM_BOT_TOKEN")


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi! I'm a summarizer bot. Send me a message and I'll summarize it for you."
    )


def summarize(update, context):
    """Summarize the message sent to the bot."""
    update.message.reply_text("Summarizing...")
    message_text = update.message.text
    summary = extract_and_summarize(message_text)
    update.message.reply_text(summary)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, summarize))
    logger.info("Starting bot")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
