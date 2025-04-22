from googleapiclient.discovery import build
from loguru import logger
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi


class VideoDetails(BaseModel):
    id: str
    title: str
    description: str
    channel_name: str
    duration: str
    transcription: str


def get_video_details(video_id: str, youtube_api_key: str) -> VideoDetails:
    logger.info(f"Getting video details from YouTube API [{video_id}]")
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    video = youtube.videos().list(part="snippet,contentDetails", id=video_id).execute()

    response = video['items'][0]
    logger.info(f"Getting video transcription [{video_id}]")
    transcript = YouTubeTranscriptApi().fetch(video_id, ('en', 'pl'))
    transcription = " ".join([t.text for t in transcript])

    return VideoDetails(
        id=video_id,
        title=response['snippet']['title'],
        description=response['snippet']['description'],
        channel_name=response['snippet']['channelTitle'],
        duration=response['contentDetails']['duration'],
        transcription=transcription
    )
