# main.py

import os
from src.cli import app

os.environ["G_MESSAGES_DEBUG"] = "none"

if __name__ == "__main__":
    app()
