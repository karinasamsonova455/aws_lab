import os
import boto3
from botocore.exceptions import ClientError

s3  = boto3.client("s3",  region_name = "eu-north-1")

def create_bucket(bucket_name, region=s3.meta.region_name):
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},
        )
        print(f"[OK] Бакет {bucket_name} створено.")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "BucketAlreadyOwnedByYou":
            print(f"[WARN] Бакет {bucket_name} вже є.")
        elif code == "BucketAlreadyExists":
            print(f"[ERROR] Ім'я {bucket_name} зайняте.")

        else:
            print(f"[ERROR] Не вдалося створити бакет: {e}")


def list_buckets():
    try:
        response = s3.list_buckets()
        print("Existing buckets:")
        for bucket in response["Buckets"]:
            print(f"  {bucket['Name']}")
    except ClientError as e:
        print(f"[ERROR] Не вдалося отримати список бакетів: {e}")


def upload_file(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3.upload_file(Filename=file_name, Bucket=bucket_name, Key=object_name)
        print(f"[OK] Файл {file_name} -> s3://{bucket_name}/{object_name}")
    except ClientError as e:
        print(f"[ERROR] Не вдалося завантажити файл: {e}")


def download_file(bucket_name, object_name, local_path):
    try:
        s3.download_file(Bucket=bucket_name, Key=object_name, Filename=local_path)
        print(f"[OK] s3://{bucket_name}/{object_name} -> {local_path}")
    except ClientError as e:
        print(f"[ERROR] Не вдалося завантажити файл: {e}")


def list_objects(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response.get("Contents", []):
            print(f"  {obj['Key']} ({obj['Size']} bytes)")
    except ClientError as e:
        print(f"[ERROR] Не вдалося отримати список об'єктів: {e}")


def empty_bucket(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
        if objects:
            s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})
            print(f"[OK] Видалено {len(objects)} об'єктів із {bucket_name}.")
        else:
            print(f"[INFO] Бакет {bucket_name} вже порожній.")
    except ClientError as e:
        print(f"[ERROR] Не вдалося очистити бакет: {e}")


def destroy_bucket(bucket_name):
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"[OK] Бакет {bucket_name} видалено.")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "NoSuchBucket":
            print(f"[WARN] Бакет {bucket_name} не існує.")
        elif code == "BucketNotEmpty":
            print(f"[ERROR] Бакет {bucket_name} не порожній.")
        else:
            print(f"[ERROR] Не вдалося видалити бакет: {e}")
