import json
from crypto.ecc_utils import ECC_encrypt

# Minimal trapdoor content for delete
trapdoor_dict = {
    "type": "delete",
    "role": "doctor",          # User's role
    "file_id": "file_c38cdc4f" # File index to delete
}

# Encrypt the trapdoor using ECC
with open("server_public_key.pem", "rb") as f:
    ECC_PUBLIC_KEY = f.read().decode()

plaintext = json.dumps(trapdoor_dict).encode()
encrypted = ECC_encrypt(plaintext, ECC_PUBLIC_KEY)

# Save to file
with open("trapdoor_delete.bin", "wb") as f:
    f.write(encrypted)

print("✅ Trapdoor for DELETE operation saved as 'trapdoor_delete.bin'")