from sqlalchemy import Column, Integer, String
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), nullable=False)
