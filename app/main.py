from fastapi import FastAPI
from app.routers import users, items
from app.database.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def read_root():
    return {"message": "Hello, this is the Grocery API!"}
from app.routers import auth

app.include_router(auth.router)
