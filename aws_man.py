import sys
import os

from modules.key import create_key_pair, delete_key_pair
from modules.ec2 import create_instance, get_public_ip, start_instance, stop_instance, reboot_instance, terminate_instance
from modules.s3 import create_bucket, list_buckets, upload_file, download_file, list_objects, empty_bucket, destroy_bucket

if __name__ == "__main__":
    func_name = sys.argv[1]
    args = sys.argv[2:]
    func = globals()[func_name]
    result = func(*args)
    if result is not None:
        print(result)