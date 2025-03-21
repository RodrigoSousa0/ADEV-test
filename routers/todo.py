from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.todo import Todo
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/todos", tags=["todos"])

class TodoSchema(BaseModel):
    id: int
    task: str
    due_date: datetime

    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    task: str
    due_date: datetime

@router.get("/", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@router.post("/", response_model=TodoSchema)
def add_todo(item: TodoCreate, db: Session = Depends(get_db)):
    new_id = int(datetime.now().timestamp())  # auto-generated
    todo = Todo(id=new_id, task=item.task, due_date=item.due_date)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}", response_model=TodoSchema)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return todo
