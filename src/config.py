import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class AppConfig:
    """A central hub for all project configurations."""
    PORT = os.getenv("PORT") or 5000
    BASE_DIR = Path(__file__).parent
    TEMPLATE_DIR = BASE_DIR / "web/templates"
    STATIC_DIR = BASE_DIR / "web/static"