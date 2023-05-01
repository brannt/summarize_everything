# Summarize Everything!

This is a PoC of a library that would convert any media into bullet points.
This PoC supports only YouTube videos (transcribed with OpenAI Whisper) and text.
OpenAI GPT 3.5-turbo is used for summarization.

## Usage
```:python
from summarizer.core import extract_and_summarize

extract_and_summarize(youtube_url_or_text)
```

## Telegram bot
An integration with a basic Telegram bot using long-polling si included. 
You can send URLs and articles to the bot. To run the bot, install the package locally
and run
```
python summarizer/integrations/telegram/bot.py
```

## Configuration
Done with env variables or .env files. OPENAI_API_KEY variable needs to be set to use the library.
SUMMARIZER_TELEGRAM_BOT_TOKEN variable needs to be set to run the bot.

## TODOs:
- More sources: web article links, podcasts, media files, chat threads, etc.
- Webhook implementation of the Telegram bot to be run serverless on Vercel/Lambda
- More integrations: other messenger bots, webapp?
- Better management of configurations and API keys
- Multi-tenant mode for integrations: allow each user to provide their own API key
- Set up tests and CI
