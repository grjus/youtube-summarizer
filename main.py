import argparse
import os
from argparse import ArgumentParser
from datetime import datetime

import boto3
from loguru import logger
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient

from app_types import YoutubeSummaryResponse, YoutubeSummary
from prompt import MODEL_ID, get_user_prompt, get_system_prompt, INFERENCE_CONFIG, TOOL_CONFIGURATION, TOOL_NAME
from secrets import get_secret
from youtube import VideoDetails, get_video_details

client: BedrockRuntimeClient = boto3.client('bedrock-runtime', region_name='eu-west-1')


def call_for_summary(video_details: VideoDetails) -> YoutubeSummaryResponse:
    logger.info(f"Calling Bedrock API for summary [{video_details.id}]")
    try:
        response = client.converse(
            modelId=MODEL_ID,
            messages=[get_user_prompt(video_details.transcription)],
            system=[get_system_prompt()],
            inferenceConfig=INFERENCE_CONFIG,
            toolConfig=TOOL_CONFIGURATION
        )
        results = filter(lambda x: x["toolUse"]["name"] == TOOL_NAME, response["output"]["message"]["content"])
        results = next(results)['toolUse']['input']
        return YoutubeSummaryResponse(summary=results['summary'], genre=results['genre'], usage=response['usage'],
                                      metrics=response['metrics'])
    except Exception as e:
        logger.error(f"Error calling Bedrock API: {e}")


def store_results(data: YoutubeSummary):
    path = os.getcwd()
    dir_path = f"{path}/.data"

    def _create_directory_if_not_exists():
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    _create_directory_if_not_exists()
    file_name = f"{int(datetime.now().timestamp() * 1000)}_{data.id}"
    with open(f"{dir_path}/{file_name}.json", "w") as f:
        f.write(data.model_dump_json(indent=2))
    logger.info(f"Results stored in {dir_path}/{file_name}.json")


def main(video_id: str, api_key: str):
    video_details = get_video_details(video_id, api_key)
    bedrock_response = call_for_summary(video_details)
    return YoutubeSummary(
        id=video_details.id,
        title=video_details.title,
        channel_name=video_details.channel_name,
        summary=bedrock_response.summary,
        genre=bedrock_response.genre,
        usage=bedrock_response.usage,
        metrics=bedrock_response.metrics,
        transcription=video_details.transcription
    )


if __name__ == "__main__":
    youtube_secret = get_secret("YtApiKey")
    args = ArgumentParser()
    args.add_argument("--video_id", type=str, help="Youtube video ID", required=True)
    args.add_argument("--store_results", action=argparse.BooleanOptionalAction)
    args = args.parse_args()
    response = main(args.video_id, youtube_secret['API_KEY'])
    if args.store_results:
        store_results(response)
