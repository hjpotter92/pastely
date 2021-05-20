import json
import logging
from base64 import b64decode
from dataclasses import dataclass
from os import getenv
from typing import Union

import boto3
from argon2 import PasswordHasher

logger = logging.getLogger(__name__)
hasher = PasswordHasher()


@dataclass
class Config:
    DYNAMODB_TABLE = getenv("PASTELY_DYNAMODB_TABLE")
    S3_BUCKET = getenv("PASTELY_S3_BUCKET")


def get_auth_password(headers: dict) -> Union[None, str]:
    auth: Union[str, None] = headers.get("authorization")
    if not (auth and auth.startswith("Token ")):
        return None
    token = auth.split(" ")[-1]
    password = b64decode(token)
    return password.decode("utf-8")


def get_s3_object(key: str):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(Config.S3_BUCKET)
    obj = bucket.Object(key)
    return obj.get()


def retrieve_content(item: dict):
    if not item.get("shortener"):
        content = get_s3_object(item["id"])
        item["content"] = content["Body"].read().decode("utf-8")
    for key in {
        "passphrase",
    }:
        if key in item:
            del item[key]
    return item


def handler(event: dict, context):
    logger.info(
        "Received event '%s' with context: %s",
        event["requestContext"]["requestId"],
        context,
    )
    paste_id = event["pathParameters"]["id"]
    headers = event["headers"]
    logger.info("Fetching information for paste id: %s", paste_id)
    db = boto3.resource("dynamodb")
    table = db.Table(Config.DYNAMODB_TABLE)
    item = table.get_item(Key={"id": paste_id})["Item"]
    if not item.get("private"):
        return retrieve_content(item)
    passphrase = get_auth_password(headers)
    if passphrase is None:
        return {
            "statusCode": 401,
            "body": json.dumps("The content is restricted! Provide passphrase."),
        }
    if hasher.verify(item["passphrase"], passphrase):
        return retrieve_content(item)
    else:
        return {
            "statusCode": 403,
            "body": json.dumps("The provided password is incorrect."),
        }
