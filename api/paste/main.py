"""
Parse content received in HTTP POST and save to dynamodb.

The content received will be of the format:

{
    "shortener": true,
    "title": "title",
    "syntax": "python",
    "content": "def test():\n    pass",
    "private": true,
    "expiry": "24",
    "passphrase": "password"
}
"""

import datetime
import json
import logging
from dataclasses import dataclass
from json import loads
from os import getenv
from string import ascii_letters, digits

import boto3
import nanoid
from argon2 import PasswordHasher
from schema import And, Optional, Or, Schema, Use

logger = logging.getLogger(__name__)
generate = lambda: nanoid.generate(ascii_letters + digits, 10)
hasher = PasswordHasher()


def validate_field(data: dict):
    if data.get("private"):
        if not data.get("passphrase"):
            raise Exception
        data["passphrase"] = hasher.hash(data["passphrase"])
    return data


def is_true(value: str) -> bool:
    if isinstance(value, str):
        return value.lower() in {"true", True, "yes", "y"}
    return bool(value)


def get_cron_expression(date: datetime.datetime) -> str:
    return f"cron({date.minute} {date.hour} {date.day} {date.month} ? {date.year})"


@dataclass
class Config:
    DYNAMODB_TABLE = getenv("PASTELY_DYNAMODB_TABLE")
    S3_BUCKET = getenv("PASTELY_S3_BUCKET")
    DELETE_LAMBDA_ARN = getenv("PASTELY_DELETE_LAMBDA_ARN")
    SCHEMA = Schema(
        And(
            Use(loads),
            {
                Optional("shortener"): Or(None, Use(is_true)),
                Optional("title"): Or(And(str, len), ""),
                Optional("syntax", default="plaintext"): And(str, len),
                "content": And(str, len),
                Optional("private"): Use(is_true),
                Optional("expiry", default=0): And(
                    Use(int),
                    Or(0, 1, 2, 6, 12, 24, 144, 288, 730, 1460, 4383, 8766),
                ),
                Optional("passphrase"): Or(And(str, len), ""),
            },
            Use(validate_field, error="Invalid data structure."),
        )
    )


def put_data_to_dynamodb(id_, **data: dict):
    db = boto3.resource("dynamodb")
    table = db.Table(Config.DYNAMODB_TABLE)
    logger.info("Putting items to dynamodb.")
    if not data.get("shortener"):
        del data["content"]
    return table.put_item(
        Item={
            "id": id_,
            **data,
        }
    )


def put_data_to_s3(name, **data: dict):
    content = data.pop("content")
    params = {
        "Key": name,
        "Metadata": {
            key: str(value)
            for key, value in data.items()
            if key not in {"content", "passphrase"}
        },
    }
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(Config.S3_BUCKET)
    if "expiry" in data:
        now = datetime.datetime.utcnow()
        params["Expires"] = now + datetime.timedelta(hours=float(data["expiry"]))
    logger.info("putting file into S3 bucket.")
    return bucket.put_object(
        Body=content,
        **params,
    )


def add_deletion_trigger_event(data: dict):
    events = boto3.client("events")
    _id = data["id"]
    created = datetime.datetime.fromisoformat(data["created_at"])
    expiry = created + datetime.timedelta(hours=data["expiry"])
    rule_name = f"pastely-delete-{_id}"
    events.put_rule(
        Name=rule_name,
        ScheduleExpression=get_cron_expression(expiry),
        Description=f"Delete the pastely object '{_id}' at {expiry.isoformat()}",
    )
    events.put_targets(
        Rule=rule_name,
        Targets=[
            {
                "Id": "1",
                "Arn": Config.DELETE_LAMBDA_ARN,
                "Input": json.dumps({"id": _id}),
            }
        ],
    )


def handler(event: dict, context):
    logger.info(
        "Received event '%s' with context: %s",
        event["requestContext"]["requestId"],
        context,
    )
    body = Config.SCHEMA.validate(event["body"])
    paste_id = generate()
    data = {
        "id": paste_id,
        "created_at": datetime.datetime.utcnow().isoformat(),
        **body,
    }
    put_data_to_dynamodb(paste_id, **data)
    if not data.get("shortener"):
        logger.info("Request to upload file to S3.")
        put_data_to_s3(paste_id, **data)
    if data["expiry"] > 0:
        add_deletion_trigger_event(data)
    return {
        "id": paste_id,
    }
