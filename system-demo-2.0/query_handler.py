import argparse
import json
from operations.insert import insert_operation
from operations.search import search_operation
from operations.update import update_operation
from operations.delete import delete_operation
from crypto.ecc_utils import ECC_decrypt
from crypto.aes_utils import AES_decrypt
from hive_interface import load_index_directory, load_keyword_index
from hdfs_interface import init_hdfs, read_file_from_hdfs, write_file_to_hdfs
import base64
# ----------------------
# Dispatcher Logic
# ----------------------

def forward_to_operation(trapdoor, AES_KEY_KEYWORD, ECC_PRIVATE_KEY):
    # External store loads
    IndexDirectory = load_index_directory()
    AES_KEY_FILE = base64.b64decode(
        'eb6b940858e887abcf26e0d9488e449b491e1b31a47f0b6ab54b8e7f8b13703b'
    )[:32]
    # Validate and extract role
    role = trapdoor.get("role")
    if not role:
        print("[Warning] No role found in trapdoor. Using 'doctor' as default.")
        role = "doctor"  # Make sure this table exists in Hive: keyword_index_doctor
    
    # Load keyword index for the role
    KeywordIndex = load_keyword_index(role.lower())

    # Dispatch operation
    op_type = trapdoor.get("type")
    keys = [AES_KEY_FILE, AES_KEY_KEYWORD, ECC_PRIVATE_KEY]
    
    if op_type == "insert":
        return insert_operation(trapdoor, IndexDirectory, KeywordIndex, *keys)
    elif op_type == "search":
        return search_operation(trapdoor, IndexDirectory, KeywordIndex, *keys)
    elif op_type == "update":
        return update_operation(trapdoor, IndexDirectory, KeywordIndex, *keys)
    elif op_type == "delete":
        return delete_operation(trapdoor, IndexDirectory, KeywordIndex)
    else:
        raise ValueError(f"Unknown operation type: {op_type}")

# ----------------------
# Query Handler
# ----------------------

def query_handler(encrypted_trapdoor_bytes, AES_KEY_KEYWORD, ECC_PRIVATE_KEY):
    decrypted = ECC_decrypt(encrypted_trapdoor_bytes, ECC_PRIVATE_KEY)
    trapdoor = json.loads(decrypted.decode())

    if "file" in trapdoor and "session_key" in trapdoor:
        print("[Handler] Decrypting file with session key...")
        session_key = bytes.fromhex(trapdoor["session_key"])
        file_hex = trapdoor["file"]
        if isinstance(file_hex, bytes):
            file_hex = file_hex.decode()
        encrypted_file = bytes.fromhex(file_hex)
        trapdoor["file"] = AES_decrypt(encrypted_file, session_key)


    return forward_to_operation(trapdoor, AES_KEY_KEYWORD, ECC_PRIVATE_KEY)

# ----------------------
# CLI Entry Point
# ----------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trapdoor", required=True, help="Path to ECC-encrypted trapdoor file")
    args = parser.parse_args()

    AES_KEY_KEYWORD = base64.b64decode(
        "HnTLt0nR3gwBfc2PU+RSfqi4hPnm/Z9p09CGYOLFMk9VFwNQIYN4/+Hluz73qq7W"
    )[:32]


    with open("server_private_key.pem", "rb") as f:
        ECC_PRIVATE_KEY = f.read().decode()

    with open(args.trapdoor, "rb") as f:
        encrypted_trapdoor_bytes = f.read()

    print("[Server] Decrypting and processing trapdoor...")
    result = query_handler(encrypted_trapdoor_bytes, AES_KEY_KEYWORD, ECC_PRIVATE_KEY)
    print("[Server] Operation Result:", result)
