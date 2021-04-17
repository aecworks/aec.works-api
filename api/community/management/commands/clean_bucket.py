import boto3
from django.conf import settings
from django.core.management.base import BaseCommand

from api.images.models import ImageAsset


class Command(BaseCommand):
    help = "Clean Unreferenced Bucket Fileds"

    def handle(self, *args, **options):
        referenced_files = set([i.file.name for i in ImageAsset.objects.all()])
        print(f"{len(referenced_files)} References files")

        access_key_id = settings.AWS_ACCESS_KEY_ID
        secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix="images")

        s3_files = set()
        for page in pages:
            for obj in page.get("Contents", []):
                s3_files.add(obj["Key"])
        print(f"{len(s3_files)} S3 files")

        unreferenced_s3_files = s3_files - referenced_files
        print(f"{len(unreferenced_s3_files)} Unreferenced S3 files")

        if unreferenced_s3_files:
            print("Cleaning bucket...")
            for key in unreferenced_s3_files:
                s3.delete_object(Bucket=bucket, Key=key)
            print("Done")

        else:
            print("No Files to clean")
