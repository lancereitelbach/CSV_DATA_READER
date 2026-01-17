import os

from pathlib import Path

class Config:

    # Path(__file__)           → /home/user/project/src/app/config.py
    # .parent                  → /home/user/project/src/app/
    # .parent                  → /home/user/project/src/
    # .parent                  → /home/user/project/  ← This is BASE_DIR (root)
    BASE_DIR = Path(__file__).parent.parent.parent

    # Directory for storing data files
    DATA_DIR = BASE_DIR / "data"
    UPLOADS_DIR = DATA_DIR/ "uploads"
    DB_PATH = DATA_DIR / "database.db"

    # Secret key for session management and other security-related needs
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")

    # Maximum allowed payload to 16 megabytes.
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for file uploads

    # Allowed file extensions for uploads
    ALLOWED_EXTENSIONS = {"csv"}

    @classmethod
    def ensure_data_directories(cls):

        """Ensure that the data directories exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)




   

