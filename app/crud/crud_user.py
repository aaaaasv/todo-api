from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.schemas import user as schemas_user
from app.models.user import User
from app import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CRUDUser:
    def __init__(self, model):
        self.model = model

    def create(self, db: Session, user: schemas_user.UserCreate):
        user_db = self.model(username=user.username, password=self.get_password_hash(user.password))
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db

    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def get_password_hash(self, plain_password: str):
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def authenticate(self, db: Session, username: str, password: str):
        user = self.get_by_username(db, username)
        if not user or not self.verify_password(plain_password=password, hashed_password=user.password):
            return False
        return user


user = CRUDUser(User)
