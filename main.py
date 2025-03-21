from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import database as db
from routers.todo import router as todo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.start_db()
    yield

app = FastAPI(lifespan=lifespan, dependencies=[Depends(db.get_db)])
app.include_router(todo_router)

@app.get("/")
async def root():
    return {"message": "Todo API is live"}
