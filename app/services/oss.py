def upload_file_to_oss(filename: str, content: bytes) -> str:
    """Stub: upload content to OSS and return an oss_key."""
    # In production, call SDK to upload and return key. Here return a fake key.
    return f"oss://bucket/{filename}"
