from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
from app.config import DATABASE_URL, REDIS_HOST

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis setup
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
