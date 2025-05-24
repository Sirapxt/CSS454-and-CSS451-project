import os
HDFS_ROOT = "/home/hadoop/secure_encrypted_db/collect_data"

def init_hdfs():
    os.makedirs(HDFS_ROOT, exist_ok=True)
    return HDFS_ROOT

def write_file_to_hdfs(file_id, data):
    path = os.path.join(HDFS_ROOT, f"{file_id}.enc")
    with open(path, "wb") as f:
        f.write(data)
    return path

def read_file_from_hdfs(file_id):
    path = os.path.join(HDFS_ROOT, f"{file_id}.txt.enc")
    with open(path, "rb") as f:
        return f.read()

def delete_file_from_hdfs(file_id):
    path = os.path.join(HDFS_ROOT, f"{file_id}.txt.enc")
    os.remove(path)
