import contextlib
import os
import tempfile
from typing import Tuple

import dotenv
import openai
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from goose3 import Goose

dotenv.load_dotenv()

from .types import SourceType

# TODO better key management
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_text(source: str) -> Tuple[str, SourceType]:
    """Extract text from a source."""
    if source.startswith("https://www.youtube.com/watch?v=") or source.startswith("https://youtu.be/"):
        return youtube_extract_transcriptapi(source), SourceType.VIDEO
    elif source.startswith("http://") or source.startswith("https://"):
        # assume it's an article
        return html_extract_goose3(source), SourceType.ARTICLE
    elif len(source) >= 1000:
        return source, SourceType.ARTICLE
    # TODO: Add support for web article links, podcasts, media files, etc.
    else:
        raise NotImplementedError(f"Source {source} not supported.")

# --- YouTube extraction ---
def youtube_extract_whisper(video_url):
    with youtube_get_audio(video_url) as audio_file:
        return extract_text_from_audio(audio_file)

def youtube_extract_transcriptapi(video_url):
    if video_url.startswith("https://youtu.be/"):
        video_id = video_url.split('/')[-1]
    else:
        video_id = video_url.split('=')[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = next(iter(transcript_list)).fetch()
    return TextFormatter().format_transcript(transcript)
    
@contextlib.contextmanager
def youtube_get_audio(video_url):
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": temp_dir + '/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            filename_collector = FilenameCollectorPP()
            ydl.add_post_processor(filename_collector)
            info = ydl.extract_info(video_url, download=False)
            ydl.process_info(info) 
            filenames = filename_collector.filenames

        with open(filenames[0], 'rb') as audio_file:
            yield audio_file

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information['filepath'])
        return [], information

def extract_text_from_audio(audio_file):
        return openai.Audio.transcribe("whisper-1", file=audio_file)

# --- HTML extraction ---
def html_extract_goose3(url):
    g = Goose()
    article = g.extract(url=url)
    return article.cleaned_text