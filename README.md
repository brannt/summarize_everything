# Summarize Everything!

This is a PoC of a library that would convert any media into bullet points.
This PoC supports YouTube videos (transcribed with ~~OpenAI Whisper~~ YouTube Transcript API),
HTML articles (extracted with Goose3) and text.
OpenAI GPT 3.5-turbo is used for summarization.

## Usage
```:python
from summarizer.core import extract_and_summarize

extract_and_summarize(youtube_url_or_text)
```

## Telegram bot
An integration with a basic Telegram bot using long-polling is included. 
You can send URLs and articles to the bot. To run the bot, install the package locally
and run
```
python summarizer/integrations/telegram/bot.py
```

## Configuration
Done with env variables or .env files. 
OPENAI_API_KEY variable needs to be set to use the library.
SUMMARIZER_TELEGRAM_BOT_TOKEN variable needs to be set to run the bot.
Enable BOT_DEBUG variable to receive debug messages about errors from the bot

## TODOs:
- This PoC has some limitations: long texts don't fit into GPT 3.5 context window and/or Vercel 10s limit
- Test other models for summarization and audio extraction
- More sources: ~~web article links~~, podcasts, media files, chat threads, etc.
- More integrations: other messenger bots, webapp?
- Better management of configurations and API keys
- Multi-tenant mode for integrations: allow each user to provide their own API key
- Set up tests and CI
