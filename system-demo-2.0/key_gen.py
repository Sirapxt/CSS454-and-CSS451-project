from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Generate private key
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Save private key
with open("server_private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    ))

# Save public key
with open("server_public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("[KeyGen] ECC key pair generated and saved.")

