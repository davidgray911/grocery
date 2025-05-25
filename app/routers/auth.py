from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.database.database import SessionLocal
from app.schemas import schemas
from app.crud import crud
from app.utils import auth, jwt_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# Funkcja do łączenia się z bazą danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rejestracja użytkownika
@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = auth.hash_password(user.password)
    return crud.create_user(db, user.username, hashed_password)

# Logowanie i zwracanie tokenu
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = jwt_token.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
