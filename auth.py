from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
import jwt
import bcrypt
from app.config import SECRET_KEY

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/signup")
async def signup(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(username=username, password_hash=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

@auth_router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256")
    return {"token": token}
