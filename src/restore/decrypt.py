from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def decrypt_file(ciphertext, encryption_metadata, master_key):
    file_key_nonce = bytes.fromhex(encryption_metadata['file_key_nonce'])
    wrapped_key = bytes.fromhex(encryption_metadata['wrapped_key'])
    nonce = bytes.fromhex(encryption_metadata['nonce'])

    master_aesgcm = AESGCM(master_key)
    file_key = master_aesgcm.decrypt(file_key_nonce, wrapped_key, associated_data=None)

    aesgcm = AESGCM(file_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return plaintext
