import os
import json
from src.restore.download import download_object
from src.restore.decrypt import decrypt_file
from src.crypto.key_derivation import derive_master_key
from src.backup.hashing import sha256_hash_file
from src.cloud.s3_client import S3Client
from src.utils.logger import setup_logger
import getpass

logger = setup_logger()

def restore_files(config, aws_access_key, aws_secret_key, manifest_path, restore_dir):
    bucket = config['aws']['bucket']
    salt_hex = config['encryption']['passphrase_salt']

    passphrase = getpass.getpass("Enter encryption passphrase: ")
    master_key = derive_master_key(passphrase, salt_hex)

    s3_client = S3Client(aws_access_key, aws_secret_key, config['aws']['region'])

    with open(manifest_path, "r") as mf:
        manifest = json.load(mf)

    os.makedirs(restore_dir, exist_ok=True)

    for entry in manifest:
        rel_path = entry['relative_path']
        s3_key = entry['s3_key']
        expected_hash = entry['sha256']
        enc_metadata = entry['encryption_metadata']

        logger.info(f"Restoring file: {rel_path} from S3 key: {s3_key}")

        ciphertext, s3_metadata = download_object(s3_client, bucket, s3_key)

        try:
            plaintext = decrypt_file(ciphertext, enc_metadata, master_key)
        except Exception as e:
            logger.error(f"Decryption failed for {rel_path}: {str(e)}")
            continue

        actual_hash = sha256_hash_file_write(plaintext)
        if actual_hash != expected_hash:
            logger.error(f"Integrity check failed for {rel_path}: expected {expected_hash}, got {actual_hash}")
            continue

        restore_path = os.path.join(restore_dir, rel_path)
        os.makedirs(os.path.dirname(restore_path), exist_ok=True)

        with open(restore_path, "wb") as f:
            f.write(plaintext)

        logger.info(f"Successfully restored: {rel_path}")


def sha256_hash_file_write(data_bytes):
    import hashlib
    sha256 = hashlib.sha256()
    sha256.update(data_bytes)
    return sha256.hexdigest()
