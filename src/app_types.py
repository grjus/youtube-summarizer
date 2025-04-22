from enum import StrEnum

from mypy_boto3_bedrock_runtime.type_defs import TokenUsageTypeDef, ConverseMetricsTypeDef
from pydantic import Field, BaseModel


class VideoGenre(StrEnum):
    POLITICS = "POLITICS"
    ENTERTAINMENT = "ENTERTAINMENT"
    MUSIC = "MUSIC"
    GAMING = "GAMING"
    SCIENCE = "SCIENCE"
    SZURIA = "SZURIA"
    OTHER = "OTHER"


class YoutubeSummaryResponse(BaseModel):
    summary: list[str] = Field(..., description="Summary of the transcription", min_length=4, max_length=8)
    genre: VideoGenre = Field(..., description="Genre of the video")
    usage: TokenUsageTypeDef = Field(..., description="Token usage information")
    metrics: ConverseMetricsTypeDef = Field(..., description="Metrics information")


class YoutubeSummary(YoutubeSummaryResponse):
    id: str = Field(..., description="Youtube video ID")
    title: str = Field(..., description="Youtube video title")
    channel_name: str = Field(..., description="Youtube channel name")
    transcription: str = Field(..., description="Youtube video transcription")
