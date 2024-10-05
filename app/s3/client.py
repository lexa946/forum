from contextlib import asynccontextmanager
from aiobotocore.session import get_session

from app.config import settings


class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as s3_client:
            yield s3_client


    async def upload_file(self, key, body) -> None:
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=key, Body=body)
            return f"{self.config['endpoint_url']}/{self.bucket_name}/{key}"


s3_client = S3Client(
    access_key=settings.S3_ACCESS_KEY,
    secret_key=settings.S3_SECRET_KEY,
    endpoint_url=settings.S3_ENDPOINT_URL,
    bucket_name=settings.S3_BUCKET_NAME
)
