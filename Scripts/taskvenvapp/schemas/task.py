from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str
    status: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: bool | None = None

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy