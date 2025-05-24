import os
from crypto.aes_utils import AES_encrypt, AES_decrypt, AES_encrypt_deterministic
from hashlib import sha256
import ast

def search_operation(trapdoor, IndexDirectory, KeywordIndex, AES_KEY_FILE, AES_KEY_KEYWORD, ECC_PRIVATE_KEY):
    roles = trapdoor["role"]
    keywords = trapdoor["keyword"]
    pubkey = trapdoor["pubkey"]
    result_ids = set()

    # hash keywords server-side
    hashed_keywords = []
    keyW = ast.literal_eval(keywords) 
    for kw in keyW:
        enc_kw = AES_encrypt_deterministic(kw.encode(), AES_KEY_KEYWORD)
        print(f"[Search] enc keywords = {enc_kw}")
        hashed_keywords.append(sha256(enc_kw).hexdigest())
        print(f"[Search] hashed keywords = {hashed_keywords}")
    
    for keyword_hash, file_id in KeywordIndex:
        for kw in hashed_keywords:
            if keyword_hash == kw:
                result_ids.add(file_id)

    # decrypt and re-encrypt files
    results = []
    session_key = os.urandom(32)
    for file_id in result_ids:
        hdfspath = IndexDirectory[file_id]["path"]
        path = hdfspath + ".enc"
        with open(path, "rb") as f:
            enc_data = f.read()
        file_bytes = AES_decrypt(enc_data, AES_KEY_FILE)
        enc_file = AES_encrypt(file_bytes, session_key)
        results.append((file_id, enc_file))

    from crypto.ecc_utils import ECC_encrypt
    enc_session_key = ECC_encrypt(session_key, pubkey)
    return {"enc_session_key": enc_session_key, "files": results}
