import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2", region_name = "eu-north-1")


def create_instance(key_name):
    try:
        instances = ec2.run_instances(
            ImageId="ami-028e435baba892443",  ### Amazon Linux 2 AMI (ARM64) in eu-north-1
            MinCount=1,
            MaxCount=1,
            InstanceType="t3.micro",
            KeyName=key_name
        )
        instance_id = instances["Instances"][0]["InstanceId"]
        print(f"[OK] Створено інстанс: {instance_id}")
        return instance_id
    except ClientError as e:
        print(f"[ERROR] Не вдалося створити інстанс: {e}")
        

def get_public_ip(instance_id):
    try:
        reservations = ec2.describe_instances(
            InstanceIds=[instance_id]
        ).get("Reservations")
        for reservation in reservations:
            for instance in reservation['Instances']:
                ip = instance.get("PublicIpAddress")
                if ip:
                    print(f"[OK] Публічна IP-адреса: {ip}")
                    return ip
        print("[WARN] Публічну IP-адресу не знайдено (інстанс не запущений або ще запускається).")
        return None
    except ClientError as e:
        print(f"[ERROR] Не вдалося отримати IP: {e}")
        

def start_instance(instance_id):
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"[OK] Інстанс {instance_id} запускається.")
    except ClientError as e:
        print(f"[ERROR] Не вдалося запустити інстанс: {e}")


def stop_instance(instance_id):
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"[OK] Інстанс {instance_id} зупиняється.")
    except ClientError as e:
        print(f"[ERROR] Не вдалося зупинити інстанс: {e}")


def reboot_instance(instance_id):
    try:
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"[OK] Інстанс {instance_id} перезавантажується.")
    except ClientError as e:
        print(f"[ERROR] Не вдалося перезавантажити інстанс: {e}")


def terminate_instance(instance_id):
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"[OK] Інстанс {instance_id} терміновано.")
    except ClientError as e:
        print(f"[ERROR] Не вдалося термінувати інстанс: {e}")
