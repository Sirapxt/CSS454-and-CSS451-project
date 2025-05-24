from pyhive import hive
import re

# ----------------------
# Helpers
# ----------------------

def sanitize_for_hive(value):
    """Sanitize a value to be safely inserted into a Hive SQL query."""
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            value = value.hex()
    value = str(value)
    value = value.replace("\\", "\\\\").replace("'", "\\'")
    value = re.sub(r"[\x00-\x1F\x7F]", "", value)  # Remove control characters
    return value

def _to_hive_array_str(py_list):
    """Convert Python list to Hive-compatible array syntax."""
    sanitized = [f"'{sanitize_for_hive(item)}'" for item in py_list]
    return f"array({', '.join(sanitized)})"

# ----------------------
# Operations
# ----------------------

def insert_index_directory(file_id, keywords, roles, policy, path):
    print(f"[Hive] insert_index_directory: {file_id}")
    file_id = sanitize_for_hive(file_id)
    policy = sanitize_for_hive(policy)
    path = sanitize_for_hive(path)
    keywords_str = _to_hive_array_str(keywords)
    roles_str = _to_hive_array_str(roles)

    conn = hive.Connection(host="localhost", port=10000)
    cursor = conn.cursor()
    query = f"""
        INSERT INTO index_directory (file_id, keywords, roles, policy, path)
        VALUES ('{file_id}', {keywords_str}, {roles_str}, '{policy}', '{path}')
    """
    cursor.execute(query)

def update_keyword_index(role, keyword_hashes, file_id):
    print(f"Inserting into {table_name}: keyword_hash={repr(kh)}, file_id={repr(file_id)}")
    conn = hive.Connection(host="localhost", port=10000)
    cursor = conn.cursor()
    table_name = f"keyword_index_{sanitize_for_hive(role.lower())}"
    file_id = sanitize_for_hive(file_id)
    for kh in keyword_hashes:
        kh = sanitize_for_hive(kh)
        cursor.execute(
            f"INSERT INTO {table_name} (keyword_hash, file_id) VALUES ('{kh}', '{file_id}')"
        )

def delete_index_directory(file_id):
    print(f"[Hive] delete_index_directory: {file_id}")
    conn = hive.Connection(host="localhost", port=10000)
    cursor = conn.cursor()
    file_id = sanitize_for_hive(file_id)
    cursor.execute(f"DELETE FROM index_directory WHERE file_id = '{file_id}'")
 
def update_keyword_index_remove(role, keyword_hashes, file_id):

    print(f"[Hive] update_keyword_index_remove: roles={role}, file={file_id}")
    conn = hive.Connection(host="localhost", port=10000)
    cursor = conn.cursor()

    table_name = f"keyword_index_{role.lower()}"
    query = f"""
            DELETE FROM {table_name} WHERE file_id = '{file_id}'
        """
    print(f"[Query] {query.strip()}")
    cursor.execute(query)

def load_index_directory():
    conn = hive.Connection(host="localhost", port=10000)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM index_directory")
    result = cursor.fetchall()
    return {
        row[0]: {
            "file_id": sanitize_for_hive(row[0]),
            "keywords": row[1],
            "roles": row[2],
            "policy": sanitize_for_hive(row[3]),
            "path": sanitize_for_hive(row[4])
        }
        for row in result
    }

def load_keyword_index(role):
    if not role:
        raise ValueError("Invalid or missing role. Cannot load keyword index.")
    table_name = f"keyword_index_{sanitize_for_hive(role.lower())}"
    conn = hive.Connection(host="localhost", port=10000)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT keyword_hash, file_id FROM {table_name}")
        return [(sanitize_for_hive(row[0]), sanitize_for_hive(row[1])) for row in cursor.fetchall()]
    except Exception as e:
        print(f"[Hive] Failed to load table {table_name}: {e}")
        return []
