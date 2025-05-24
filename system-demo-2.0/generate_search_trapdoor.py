import json
from crypto.ecc_utils import ECC_encrypt
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# === 1. Generate random user's ECC key pair ===
user_private_key = ec.generate_private_key(ec.SECP256R1())
user_public_key = user_private_key.public_key()

# Serialize public key to PEM string
user_pubkey_pem = user_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

# === 2. Construct trapdoor ===
trapdoor = {
    "type": "search",
    "keyword": ["2mb"],
    "role": "doctor",
    "pubkey": user_pubkey_pem
}

trapdoor_bytes = json.dumps(trapdoor).encode()

# === 3. Load server's public key for encryption ===
with open("server_public_key.pem", "rb") as f:
    ECC_PUBLIC_KEY = f.read().decode()

# === 4. Encrypt the trapdoor ===
encrypted = ECC_encrypt(trapdoor_bytes, ECC_PUBLIC_KEY)

# === 5. Save to file ===
with open("trapdoor_search.bin", "wb") as f:
    f.write(encrypted)

print("[Client] Encrypted trapdoor with user pubkey saved to trapdoor_search.bin")
