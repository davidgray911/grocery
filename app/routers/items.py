from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.crud import crud
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_item_for_user(db=db, item=item, user_id=user_id)
