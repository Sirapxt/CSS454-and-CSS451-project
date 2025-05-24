from operations.file_locks import acquire_lock
from crypto.aes_utils import AES_encrypt, AES_decrypt
from crypto.ecc_utils import ECC_decrypt
from keywords.extractor import KeywordExtractor
from hashlib import sha256
from hdfs_interface import write_file_to_hdfs

def update_operation(trapdoor, IndexDirectory, KeywordIndex, AES_KEY_FILE, AES_KEY_KEYWORD, ECC_PRIVATE_KEY):
    file_id = trapdoor["file_index"]
    user_roles = trapdoor["user_roles"]
    updated_roles = trapdoor["updated_roles"]
    update_mode = trapdoor["update_mode"]

    if file_id not in IndexDirectory:
        raise FileNotFoundError("File ID does not exist")
    meta = IndexDirectory[file_id]
    if not any(r in meta["delete_update_policy"] for r in user_roles):
        raise PermissionError("Not authorized")

    lock = acquire_lock(file_id)
    try:
        old_hashes = meta["keywords"]
        old_roles = meta["roles"]
        for role in old_roles:
            for h in old_hashes:
                lst = KeywordIndex.get(role, {}).get(h, [])
                if file_id in lst:
                    lst.remove(file_id)
                    if not lst:
                        del KeywordIndex[role][h]

        if update_mode == "update_roles_only":
            for role in updated_roles:
                KeywordIndex.setdefault(role, {})
                for h in old_hashes:
                    KeywordIndex[role].setdefault(h, []).append(file_id)
            meta["roles"] = updated_roles
            return "[Update] Roles updated only."

        elif update_mode == "update_file_and_roles":
            # decrypt file from user
            session_key = ECC_decrypt(trapdoor["aes_key_enc"], ECC_PRIVATE_KEY)
            new_bytes = AES_decrypt(trapdoor["file"], session_key)

            # reindex keywords
            keywords = KeywordExtractor(new_bytes)
            new_hashes = []
            for kw in keywords:
                enc_kw = AES_encrypt(kw.encode(), AES_KEY_KEYWORD)
                new_hashes.append(sha256(enc_kw).hexdigest())
                for role in updated_roles:
                    KeywordIndex.setdefault(role, {}).setdefault(new_hashes[-1], []).append(file_id)

            # overwrite file in HDFS
            enc_file = AES_encrypt(new_bytes, AES_KEY_FILE)
            write_file_to_hdfs(file_id, enc_file)

            meta["keywords"] = new_hashes
            meta["roles"] = updated_roles
            return "[Update] File and roles updated."

        else:
            raise ValueError("Invalid update_mode")
    finally:
        lock.release()
