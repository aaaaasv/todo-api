from fastapi import FastAPI

from app.routers import items, users

app = FastAPI()

app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(items.router, prefix='/items', tags=['items'])
