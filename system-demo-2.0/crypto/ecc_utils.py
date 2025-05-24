from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def ECC_encrypt(plaintext: bytes, recipient_pubkey_pem: str) -> bytes:
    # Load recipient public key
    recipient_public_key = serialization.load_pem_public_key(recipient_pubkey_pem.encode())

    # Generate ephemeral private key
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
    shared_key = ephemeral_private_key.exchange(ec.ECDH(), recipient_public_key)

    # Derive AES key from shared secret
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'ecies').derive(shared_key)

    # Encrypt using AES (GCM mode recommended for integrity)
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(derived_key), modes.GCM(iv)).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Serialize ephemeral pubkey + IV + tag + ciphertext
    ephemeral_pubkey_bytes = ephemeral_private_key.public_key().public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint
    )

    return ephemeral_pubkey_bytes + iv + encryptor.tag + ciphertext

def ECC_decrypt(encrypted_data: bytes, private_key_pem: str) -> bytes:
    # Load system's private key
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)

    # Parse ephemeral public key, IV, tag, and ciphertext
    epk_len = 65  # Uncompressed point for SECP256R1
    iv_len = 12
    tag_len = 16

    epk_bytes = encrypted_data[:epk_len]
    iv = encrypted_data[epk_len:epk_len+iv_len]
    tag = encrypted_data[epk_len+iv_len:epk_len+iv_len+tag_len]
    ciphertext = encrypted_data[epk_len+iv_len+tag_len:]

    # Load ephemeral public key
    ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), epk_bytes)

    # Derive AES key
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'ecies').derive(shared_key)

    # Decrypt
    decryptor = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()