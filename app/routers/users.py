from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas import user as schemas_user
from app.crud import crud_user

router = APIRouter()


@router.post('/', response_model=schemas_user.User)
def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    user_db = crud_user.user.get_by_username(db, user.username)
    if user_db:
        raise HTTPException(
            detail='Username already registered',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return crud_user.user.create(db, user)


@router.post('/token')
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.user.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = crud_user.user.create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get("/me", response_model=schemas_user.User)
async def read_users_me(current_user: schemas_user.User = Depends(get_current_user)):
    return current_user
