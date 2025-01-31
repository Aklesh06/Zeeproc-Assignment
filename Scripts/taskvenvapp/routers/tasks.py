import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from ..crud.task import get_task,get_tasks,create_task,update_task,delete_task
from ..schemas.task import Task, TaskCreate, TaskUpdate
from ..database import SessionLocal
from ..llms.analyze import analyzer

router = APIRouter()
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks/", response_model=Task)
def create(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@router.get("/tasks/{task_id}", response_model=Task)
def read(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}", response_model=Task)
def update(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}", response_model=Task)
def delete(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/tasks/analyze/")
def analyze_task(description: str):
    if not description:
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    try:
        logger.info(f"Analyzing task description: {description}")
        result = analyzer.invoke({"description": description})
        logger.info(f"Category returned: {result}")
        return {"category": result}
    except Exception as e:
        logger.error(f"Error analyzing task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}