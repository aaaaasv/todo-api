from sqlalchemy.orm import Session

from app.crud import crud_item, crud_user
from app.schemas import item as schemas_item
from app.schemas import user as schemas_user


def create_user(db: Session, username: str):
    user_in = schemas_user.UserCreate(username=username, password='testpassword1')
    return crud_user.user.create(db, user=user_in)


def test_item_create(db: Session):
    owner = create_user(db, username='itemcreateuser')

    item_data = {
        'title': 'item title',
        'description': 'item description'
    }
    item_in = schemas_item.ItemCreate(**item_data)
    item = crud_item.item.create(db, item=item_in, owner_id=owner.id)
    assert item.title == item_in.title
    assert item.description == item_in.description
    assert item.owner_id == owner.id


def test_get_item(db: Session):
    owner = create_user(db, username='itemgetuser')
    item_in = schemas_item.ItemCreate(title='title test1', description='description test2')
    item = crud_item.item.create(db, item=item_in, owner_id=owner.id)

    item_db = crud_item.item.get(db, item_id=item.id)

    assert item_db.id == item.id


def test_get_user_items(db: Session):
    owner = create_user(db, username='itemsgetuser')
    item_amount = 7
    item_in = schemas_item.ItemCreate(title='title test', description='description test')
    items_in = []
    for i in range(item_amount):
        item = crud_item.item.create(db, item=item_in, owner_id=owner.id)
        items_in.append(item)

    items_db = crud_item.item.get_owner_collection(db, owner_id=owner.id)
    assert len(items_db) == item_amount
    assert items_in == items_db


def test_update_item(db: Session):
    owner = create_user(db, username='itemupdateuser')
    item_in = schemas_item.ItemCreate(title='title test1', description='description test2')
    item_db = crud_item.item.create(db, item=item_in, owner_id=owner.id)

    item_update_in = schemas_item.ItemUpdate(title='newtitle', description='newdescription')

    item_update_db = crud_item.item.update(db, db_item=item_db, update_item=item_update_in)

    assert item_update_db.description == item_update_in.description
    assert item_update_db.title == item_update_in.title


def test_delete_item(db: Session):
    owner = create_user(db, username='itemdeleteuser')
    item_in = schemas_item.ItemCreate(title='title test1', description='description test2')
    item_db = crud_item.item.create(db, item=item_in, owner_id=owner.id)
    item_id = item_db.id

    crud_item.item.delete(db, item=item_db)

    item_db = crud_item.item.get(db, item_id=item_id)

    assert item_db is None
