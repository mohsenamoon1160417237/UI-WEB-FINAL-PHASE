from typing import Optional
import boto3

from django.conf import settings


def arvan_auth() -> Optional[boto3.resource]:
    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=settings.ARVAN_ENDPOINT,
            aws_access_key_id=settings.ARVAN_ACCESS_KEY,
            aws_secret_access_key=settings.ARVAN_SECRET_KEY
        )
        return s3_resource

    except Exception as exc:
        print(f"Arvan auth error: {exc}")
