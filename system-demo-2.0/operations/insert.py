import uuid
from keywords.extractor import KeywordExtractor
from crypto.aes_utils import AES_encrypt, AES_decrypt, AES_encrypt_deterministic
from hive_interface import insert_index_directory, update_keyword_index
from hdfs_interface import write_file_to_hdfs
from hashlib import sha256

def insert_operation(trapdoor, IndexDirectory, KeywordIndex, AES_KEY_FILE, AES_KEY_KEYWORD, ECC_PRIVATE_KEY):
    # === Step 1: Auto-generate file ID ===
    file_id = f"file_{uuid.uuid4().hex[:8]}"
    print("[Insert] File ID gen")

    # === Step 2: Decrypt file ===
    plaintext = (trapdoor["file"])
    
    # === Step 3: Extract keywords ===
    extractor = KeywordExtractor()
    keyword_hashes = []
    keywords = extractor.extract_all(plaintext.decode("utf-8", errors="ignore"))
    for kw in keywords:
        print(f"[Search] keywords = {kw}")
        enc_kw = AES_encrypt_deterministic(kw.encode(), AES_KEY_KEYWORD)
        print(f"[Search] enc keywords = {enc_kw}")
        keyword_hashes.append(sha256(enc_kw).hexdigest())
    print("[Insert] Keyword Extracted")

    cipher = AES_encrypt(plaintext, AES_KEY_FILE)

    # === Step 4: Write file to HDFS ===
    hdfs_path = f"/home/hadoop/secure_encrypted_db/collect_data/{file_id}.txt"
    write_file_to_hdfs(hdfs_path, cipher)
    print("[Insert] HDFS")

    # === Step 5: Update Index Directory and Keyword Index ===
    searchable_roles = trapdoor["searchable_roles"]
    update_roles = trapdoor["update_delete_roles"]

    insert_index_directory(
        file_id=file_id,
        keywords=list(keyword_hashes),
        roles=searchable_roles,
        policy=update_roles,
        path=hdfs_path
    )
    print("[Insert] Insert indexDirect")

    for role in searchable_roles:
        update_keyword_index(role, keyword_hashes, file_id)

    print(f"[Insert] Success: {file_id}")
    return {"file_id": file_id, "status": "inserted"}
