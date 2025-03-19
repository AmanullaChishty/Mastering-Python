# This module holds configuration settings
import os

class Settings:
    API_TITLE: str = "Asynchronous Task Manager API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_TOKEN: str = os.getenv("SECRET_TOKEN", "secrettoken")

settings=Settings()