from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='items')
