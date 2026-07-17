from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "output/pdf")