import os
import json
from src.backup.file_discovery import discover_files
from src.backup.hashing import sha256_hash_file
from src.backup.encrypt import encrypt_file
from src.cloud.s3_client import S3Client
from src.crypto.key_derivation import derive_master_key
from src.utils.logger import setup_logger
import getpass

logger = setup_logger()

def backup_all_files(config, aws_access_key, aws_secret_key):
    source_dir = config['backup']['source_dir']
    bucket = config['aws']['bucket']
    prefix = config['aws']['prefix']
    salt_hex = config['encryption']['passphrase_salt']

    passphrase = getpass.getpass("Enter encryption passphrase: ")
    master_key = derive_master_key(passphrase, salt_hex)

    s3_client = S3Client(aws_access_key, aws_secret_key, config['aws']['region'])

    manifest = []

    files = discover_files(source_dir)

    for rel_path in files:
        abs_path = os.path.join(source_dir, rel_path)
        logger.info(f"Processing file: {rel_path}")

        file_hash = sha256_hash_file(abs_path)
        ciphertext, metadata = encrypt_file(abs_path, master_key)

        s3_key = f"{prefix}/{rel_path}.enc"
        s3_client.upload(bucket, s3_key, ciphertext, metadata)

        manifest.append({
            "relative_path": rel_path,
            "sha256": file_hash,
            "s3_key": s3_key,
            "encryption_metadata": metadata
        })
        logger.info(f"Uploaded: {s3_key}")

    os.makedirs(config['backup']['manifest_dir'], exist_ok=True)
    manifest_path = os.path.join(config['backup']['manifest_dir'], "backup_manifest.json")
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=4)
    logger.info(f"Backup manifest saved to {manifest_path}")
