from sqlalchemy.orm import Session

from app.schemas import item as schemas_item
from app.models.item import Item


class CRUDItem:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, item_id: int):
        return db.query(self.model).filter(self.model.id == item_id).first()

    def get_owner_collection(self, db: Session, owner_id: int):
        return db.query(self.model).filter(self.model.owner_id == owner_id).all()

    def create(self, db: Session, item: schemas_item.ItemCreate, owner_id: int):
        item_db = self.model(title=item.title, description=item.description, owner_id=owner_id)
        db.add(item_db)
        db.commit()
        db.refresh(item_db)
        return item_db

    def update(self, db: Session, db_item: schemas_item.Item, update_item: schemas_item.ItemCreate):
        db_item.title = update_item.title
        db_item.description = update_item.description
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def delete(self, db: Session, item):
        db.delete(item)
        db.commit()
        return item


item = CRUDItem(Item)
