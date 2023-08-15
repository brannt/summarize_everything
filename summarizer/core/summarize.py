import os

import dotenv
import openai
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
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
    return summarize_langchain(text, source_type, tokens, as_type)


PROMPT_TEMPLATE = """
I will provide you a {source_type} below between START and END words.
START
{text}
END
Summarize the transcript above as a {as_type} in less than {tokens} words.
"""


def summarize_openai(
    text: str,
    source_type: str,
    tokens: int = DEFAULT_TOKEN_LIMIT,
    as_type="bullet points",
) -> str:
    transcript_prompt = PROMPT_TEMPLATE.format(
        source_type=SOURCE_TYPES[source_type], text=text, as_type=as_type, tokens=tokens
    )
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


def summarize_langchain(
    text: str,
    source_type: str,
    tokens: int = DEFAULT_TOKEN_LIMIT,
    as_type="bullet points",
) -> str:
    llm = _get_langchain_llm()
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE.format(
            source_type=SOURCE_TYPES[source_type],
            as_type=as_type,
            tokens=tokens,
            text="{text}",
        ),
        input_variables=["text"],
    )
    text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=500)
    texts = text_splitter.split_text(text)
    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        combine_prompt=prompt,
        map_prompt=prompt,
    )
    docs = [Document(page_content=t) for t in texts]
    return chain.run(docs)


def _get_langchain_llm():
    from langchain import OpenAI

    return OpenAI(temperature=0)
