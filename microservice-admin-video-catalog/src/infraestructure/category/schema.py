from sqlalchemy import Column, String, Boolean, DateTime
from infraestructure.db import Base

class CategorySchema(Base):
    __tablename__ = 'categories'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at: Column(DateTime)
    is_active = Column(Boolean, default=True)
