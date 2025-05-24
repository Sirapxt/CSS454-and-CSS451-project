from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def AES_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.nonce + cipher.encrypt(data)

def AES_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=ciphertext[:16])
    return cipher.decrypt(ciphertext[16:])

BLOCK_SIZE = 16

def AES_encrypt_deterministic(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, BLOCK_SIZE))

def AES_decrypt_deterministic(ciphertext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
