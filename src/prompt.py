from typing import Type

from mypy_boto3_bedrock_runtime.type_defs import ToolSpecificationTypeDef, MessageTypeDef, \
    InferenceConfigurationTypeDef, ToolConfigurationTypeDef, SystemContentBlockTypeDef
from pydantic import BaseModel

from src.app_types import YoutubeSummaryResponse

MODEL_ID = "eu.anthropic.claude-3-7-sonnet-20250219-v1:0"

INFERENCE_CONFIG: InferenceConfigurationTypeDef = {
    "topP": 0.9,
    "temperature": 0.1,
    "maxTokens": 4096,
}

_SYSTEM_PROMPT = """
Your task:
Given a transcript of a YouTube video inside <transcript> tag, perform **two tasks**:

1. **Generate a detailed summary** of the video written in the **same language** as the transcript (Polish or English).
2. **Classify the video** into one of the following genres. Choose **exactly one**, and return only the label (do not create new categories):

Available genres:

- POLITICS — political commentary, news, analysis, speeches, interviews with politicians
- ENTERTAINMENT — talk shows, celebrity interviews, lifestyle, comedy, general entertainment
- MUSIC — music videos, reviews, discussions, lyrics analysis
- GAMING — gameplay, game reviews, commentary, e-sports
- SCIENCE — educational content, scientific explanations, documentaries, academic lectures
- SZURIA — conspiracy theories, pseudoscience, misinformation, anti-vaccine content, chemtrails
- OTHER — use only if none of the above categories apply
"""


def pydantic_to_converse_tool(model: Type[BaseModel], name: str, description: str) -> ToolSpecificationTypeDef:
    return {
        "name": name,
        "inputSchema": {
            "json": model.model_json_schema()
        },
        "description": description
    }


def get_user_prompt(transcription: str) -> MessageTypeDef:
    return {
        "role": "user",
        "content": [{
            "text": f"<transcription>\n{transcription}\n</transcription>"
        }]
    }


def get_system_prompt() -> SystemContentBlockTypeDef:
    return {
        "text": _SYSTEM_PROMPT,
    }


TOOL_NAME = "YoutubeSummaryTool"

_TOOL_SPEC: ToolSpecificationTypeDef = pydantic_to_converse_tool(YoutubeSummaryResponse, TOOL_NAME,
                                                                 "Youtube summary response")

TOOL_CONFIGURATION: ToolConfigurationTypeDef = {
    "tools": [{
        "toolSpec": _TOOL_SPEC,
    }],
    "toolChoice": {
        "tool": {
            "name": TOOL_NAME,
        }
    }
}
