from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
