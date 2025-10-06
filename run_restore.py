import json
import os
from src.restore.restore_runner import restore_files

def main():
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
    main()
