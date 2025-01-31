from fastapi import Depends, FastAPI
from .routers import tasks
from .database import engine, Base
from .auth import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    tasks.router,
    dependencies=[Depends(get_current_user)],
)

@app.get("/")
def read_root():
    return {"message": "Task Manager API"}