import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/poker_db")
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
