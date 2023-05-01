import os

import dotenv
import openai

from .types import SourceType

dotenv.load_dotenv()
DEFAULT_TOKEN_LIMIT = 1000

SOURCE_TYPES = {
    SourceType.VIDEO: "video transcript",
    SourceType.ARTICLE: "article",
}

# TODO better key management
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize(
    text: str,
    source_type: str,
    tokens: int = DEFAULT_TOKEN_LIMIT,
    as_type="bullet points",
) -> str:
    return summarize_openai(text, source_type, tokens, as_type)


def summarize_openai(
    text: str,
    source_type: str,
    tokens: int = DEFAULT_TOKEN_LIMIT,
    as_type="bullet points",
) -> str:
    transcript_prompt = f"""
I will provide you a {SOURCE_TYPES[source_type]} below between START and END words.
START
{text}
END
Summarize the transcript above as a {as_type} in less than {tokens} words.
"""
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a superhuman assistant capable of perfectly rewriting and summarizing articles and transcripts.",
            },
            {"role": "user", "content": transcript_prompt},
        ],
        max_tokens=tokens,
    )
    return completion.choices[0].message.content
