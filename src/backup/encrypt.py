from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_file(filepath, master_key):
    file_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(file_key)
    nonce = os.urandom(12)

    with open(filepath, "rb") as f:
        plaintext = f.read()

    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    master_aesgcm = AESGCM(master_key)
    file_key_nonce = os.urandom(12)
    wrapped_key = master_aesgcm.encrypt(file_key_nonce, file_key, associated_data=None)

    metadata = {
        "nonce": nonce.hex(),
        "wrapped_key": wrapped_key.hex(),
        "file_key_nonce": file_key_nonce.hex(),
        "algorithm": "AES-GCM-256"
    }
    return ciphertext, metadata
