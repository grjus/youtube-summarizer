import json

import boto3
from loguru import logger
from mypy_boto3_secretsmanager import SecretsManagerClient

client: SecretsManagerClient = boto3.client("secretsmanager", region_name="eu-west-1")


def get_secret(secret_name: str) -> dict:
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            return json.loads(response["SecretString"])
        else:
            raise ValueError("Secret is not a string")
    except Exception as e:
        logger.error(f"Error fetching secret: {e}")
        raise
