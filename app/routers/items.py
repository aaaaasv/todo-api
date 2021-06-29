from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas import user as schemas_user
from app.schemas import item as schemas_item
from app.crud import crud_item

router = APIRouter()


@router.post('/', response_model=schemas_item.Item)
def create_item(item: schemas_item.ItemCreate, db: Session = Depends(get_db),
                current_user: schemas_user.User = Depends(get_current_user)):
    return crud_item.item.create(db, item=item, owner_id=current_user.id)


@router.get('/{item_id}', response_model=schemas_item.Item)
def get_item(item_id: int, db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    db_item = crud_item.item.get(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_item


@router.get('/', response_model=List[schemas_item.Item])
def get_items(db: Session = Depends(get_db), current_user: schemas_user.User = Depends(get_current_user)):
    items = crud_item.item.get_owner_collection(db, owner_id=current_user.id)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return items


@router.put('/{item_id}', response_model=schemas_item.Item)
def update_item(item_id: int, item_update: schemas_item.ItemUpdate, db: Session = Depends(get_db),
                current_user: schemas_user.User = Depends(get_current_user)):
    db_item = crud_item.item.get(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return crud_item.item.update(db, db_item=db_item, update_item=item_update)


@router.delete('/{item_id}', response_model=schemas_item.Item)
def update_item(item_id: int, db: Session = Depends(get_db),
                current_user: schemas_user.User = Depends(get_current_user)):
    db_item = crud_item.item.get(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return crud_item.item.delete(db, item=db_item)
