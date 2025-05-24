from threading import Lock
_file_locks = {}
_global_lock = Lock()

def acquire_lock(file_id):
    with _global_lock:
        if file_id not in _file_locks:
            _file_locks[file_id] = Lock()
        lock = _file_locks[file_id]
    if not lock.acquire(timeout=5):
        raise RuntimeError("File locked")
    return lock
