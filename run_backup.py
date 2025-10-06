import json
import os
import sys
from src.backup.backup_runner import backup_all_files
from src.restore.restore_runner import restore_files

def run_backup():
    with open("config/config.json") as f:
        config = json.load(f)

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise EnvironmentError("AWS credentials are not set in environment variables")

    backup_all_files(config, aws_access_key, aws_secret_key)


def run_restore():
    with open("config/config.json") as f:
        config = json.load(f)

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise EnvironmentError("AWS credentials are not set in environment variables")

    manifest_path = "manifests/backup_manifest.json"
    restore_dir = "data/restored"

    restore_files(config, aws_access_key, aws_secret_key, manifest_path, restore_dir)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        run_restore()
    else:
        run_backup()
