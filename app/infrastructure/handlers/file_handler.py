import os.path
import shutil
import tempfile

from starlette.datastructures import UploadFile


class FileHandler:
    """Handles saving and deleting uploaded files"""

    @staticmethod
    def save(content: str, file_path: str) -> str:
        """Saves content to a file by its path"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(file_path)

    @staticmethod
    def save_upload_tmp(upload_file: UploadFile, suffix: str) -> str:
        """Save uploaded file to a temporary local path"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            return tmp.name

    @staticmethod
    def delete_upload_tmp(path):
        """Safely deletes a temporary file if it exists"""
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except (FileNotFoundError, PermissionError, OSError) as e:
            print(f"[WARN] Failed to delete temp file {path}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")