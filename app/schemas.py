from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    priority: str
    category: str
    due_date: str


class TodoUpdate(BaseModel):
    title: str
    completed: bool
    priority: str
    category: str
    due_date: str


class TodoResponse(BaseModel):

    id: int
    title: str
    completed: bool
    priority: str
    category: str
    due_date: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):

    username: str

    email: str

    password: str

class UserUpdate(BaseModel):

    username: str

    email: str