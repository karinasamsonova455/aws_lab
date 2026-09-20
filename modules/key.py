import os
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2", region_name = "eu-north-1")

def create_key_pair(key_name = "ec2-keys"):
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]
        with os.fdopen(os.open("/tmp/aws_ec2_key.pem",
                               os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)
        print(f"[OK] Ключову пару створено: {key_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
            print(f"[WARN] Ключова пара '{key_name}' вже існує, тому... Нє.")
        else:
            print(f"[ERROR] Не вдалося створити ключову пару: {e}")


def delete_key_pair(key_name):
    try:
        ec2.delete_key_pair(KeyName=key_name)
        print(f"[OK] Ключову пару '{key_name}' видалено з AWS.")
    except ClientError as e:
        print(f"[WARN] Не вдалося видалити ключову пару: {e}")

    if os.path.exists("/tmp/aws_ec2_key.pem"):
        os.remove("/tmp/aws_ec2_key.pem")
        print(f"[OK] Локальний файл /tmp/aws_ec2_key.pem видалено.")

