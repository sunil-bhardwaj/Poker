from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Transaction

wallet_router = APIRouter(prefix="/wallet", tags=["Wallet"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@wallet_router.post("/deposit")
async def deposit(user_id: int, amount: float, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    user.balance += amount
    transaction = Transaction(user_id=user.id, amount=amount, type="deposit")
    db.add(transaction)
    db.commit()
    return {"message": "Deposit successful", "balance": user.balance}
