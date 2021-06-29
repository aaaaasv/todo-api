from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas import user as schemas_user


def test_user_create(db: Session):
    user_data = {
        'username': 'createusername',
        'password': 'testpassword1'
    }
    user_in = schemas_user.UserCreate(**user_data)
    user = crud_user.user.create(db, user=user_in)
    assert user.username == user_in.username
    assert hasattr(user, 'password')


def test_get_user_by_username(db: Session):
    user_in = schemas_user.UserCreate(username='getusernameuser', password='testpassword1')
    user = crud_user.user.create(db, user=user_in)

    user_get = crud_user.user.get_by_username(db, username=user.username)
    assert user
    assert user.id == user_get.id


def test_authenticate(db: Session):
    user_in = schemas_user.UserCreate(username='authusername', password='testpasswordright')
    crud_user.user.create(db, user=user_in)

    assert crud_user.user.authenticate(db, username=user_in.username, password=user_in.password)
    assert not crud_user.user.authenticate(db, username=user_in.username, password='wrongtestpassword')
