from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, Base, get_db
import models, schemas, crud, utils
from typing import types, List

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Decode token and get user (skipping actual implementation for brevity)
    user = crud.get_user_by_email(db, email="user@example.com")  # Placeholder
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # Create and return token (skipping actual implementation for brevity)
    return {"access_token": "fake-token", "token_type": "bearer"}

@app.post("/passwords/", response_model=schemas.Password)
def create_password(password: schemas.PasswordCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_password(db=db, password=password, user_id=current_user.id)

@app.get("/passwords/", response_model=List[schemas.Password])
def read_passwords(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_passwords(db=db, user_id=current_user.id)

@app.delete("/passwords/{password_id}")
def delete_password(password_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    crud.delete_password(db=db, password_id=password_id)
    return {"detail": "Password deleted"}
