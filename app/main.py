from fastapi import FastAPI

from app.routers import items, users
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(items.router, prefix='/items', tags=['items'])
