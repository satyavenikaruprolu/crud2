from sqlalchemy.orm import Session
import models, schemas
from utils import get_password_hash

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_password(db: Session, password: schemas.PasswordCreate, user_id: int):
    db_password = models.Password(**password.dict(), user_id=user_id)
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password

def get_passwords(db: Session, user_id: int):
    return db.query(models.Password).filter(models.Password.user_id == user_id).all()

def delete_password(db: Session, password_id: int):
    db_password = db.query(models.Password).filter(models.Password.id == password_id).first()
    db.delete(db_password)
    db.commit()
