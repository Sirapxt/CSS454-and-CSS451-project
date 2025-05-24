from hashlib import sha256
from hive_interface import delete_index_directory, update_keyword_index_remove
from hdfs_interface import delete_file_from_hdfs
import ast

def delete_operation(trapdoor, IndexDirectory, KeywordIndex):
    file_id = trapdoor["file_id"]
    user_roles = trapdoor["role"]
    if file_id not in IndexDirectory:
        raise FileNotFoundError("File not exist")
    meta = IndexDirectory[file_id]
    if not any(r in meta["policy"] for r in user_roles):
        raise PermissionError("Not authorized")

    # remove keyword references
    roles_list = ast.literal_eval(meta["roles"]) 
    for role in roles_list:
        print(role)
        update_keyword_index_remove(role, meta["keywords"], file_id)

    # delete metadata and file
    delete_index_directory(file_id)
    delete_file_from_hdfs(file_id)
    del IndexDirectory[file_id]
    return f"[Delete] File {file_id} deleted."