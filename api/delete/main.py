from dataclasses import dataclass
from os import getenv

import boto3


@dataclass
class Config:
    DYNAMODB_TABLE = getenv("PASTELY_DYNAMODB_TABLE")
    S3_BUCKET = getenv("PASTELY_S3_BUCKET")


def delete_id(_id: str):
    db = boto3.resource("dynamodb")
    s3 = boto3.resource("s3")
    events = boto3.client("events")
    table = db.Table(Config.DYNAMODB_TABLE)
    table.delete_item(Key={"id": _id})
    s3_object = s3.Object(Config.S3_BUCKET, _id)
    s3_object.delete()
    rule_name = f"pastely-delete-{_id}"
    events.remove_targets(Rule=rule_name, Ids=["1"])
    events.delete_rule(Name=rule_name)
    print("Deleted item.")


def handler(event, context):
    if event.get("id"):
        delete_id(event["id"])
