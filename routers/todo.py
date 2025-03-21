from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.todo import Todo
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/todos", tags=["todos"])

class TodoSchema(BaseModel):
    id: int
    task: str

    class Config:
        orm_mode = True

@router.get("/", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@router.post("/", response_model=TodoSchema)
def add_todo(item: TodoSchema, db: Session = Depends(get_db)):
    todo = Todo(id=item.id, task=item.task)
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
