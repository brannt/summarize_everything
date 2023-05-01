from .extract import extract_text
from .summarize import summarize

def extract_and_summarize(source: str) -> str:
    """Extract and summarize text from a source."""
    text, source_type = extract_text(source)
    return summarize(text, source_type)