import os
from dotenv import load_dotenv

load_dotenv()

CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "http://localhost")
