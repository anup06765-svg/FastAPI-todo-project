from sqlalchemy.orm import Session
from . import models
from . import schemas
from app.auth import hash_password


def create_task(
    db,
    todo,
    user_id
):

    task = models.Todo(

        title=todo.title,

        priority=todo.priority,

        category=todo.category,

        due_date=todo.due_date,

        user_id=user_id

    )

    db.add(task)

    db.commit()

    db.refresh(task)

    return task



def get_tasks(db: Session):

    return db.query(models.Todo).all()

def get_task(db: Session, task_id: int):

    return db.query(models.Todo).filter(
        models.Todo.id == task_id
    ).first()

def get_task_by_user(
    db: Session,
    task_id: int,
    user_id: int
):

    return db.query(models.Todo).filter(
        models.Todo.id == task_id,
        models.Todo.user_id == user_id
    ).first()

def update_task(
    db: Session,
    task_id: int,
    user_id: int,
    todo
):

    task = db.query(models.Todo).filter(
        models.Todo.id == task_id,
        models.Todo.user_id == user_id
    ).first()

    if task is None:
        return None

    task.title = todo.title
    task.completed = todo.completed
    task.priority = todo.priority
    task.category = todo.category
    task.due_date = todo.due_date

    db.commit()

    db.refresh(task)

    return task


def delete_task(db, task_id, user_id):

    task = db.query(models.Todo).filter(

        models.Todo.id == task_id,

        models.Todo.user_id == user_id

    ).first()

    if task:

        db.delete(task)

        db.commit()


def toggle_complete(
    db: Session,
    task_id: int,
    user_id: int
):

    task = db.query(models.Todo).filter(
        models.Todo.id == task_id,
        models.Todo.user_id == user_id
    ).first()

    if task is None:
        return None

    task.completed = not task.completed

    db.commit()

    db.refresh(task)

    return task

def search_tasks(db, search):

    query = db.query(models.Todo)

    if search:

        query = query.filter(

            models.Todo.title.contains(search)

        )

    return query.order_by(models.Todo.id.desc()).all()


def create_user(db, user):

    hashed = hash_password(
        user.password
    )

    new_user = models.User(

        username=user.username,

        email=user.email,

        password=hashed

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

def get_user_by_username(db, username):

    return db.query(models.User).filter(
        models.User.username == username
    ).first()

def get_tasks_by_user(
    db,
    user_id
):

    return db.query(models.Todo).filter(

        models.Todo.user_id == user_id

    ).order_by(

        models.Todo.id.desc()

    ).all()


def get_user_by_id(
    db,
    user_id
):

    return db.query(models.User).filter(

        models.User.id == user_id

    ).first()



def search_tasks_by_user(db, user_id, search):

    query = db.query(models.Todo).filter(
        models.Todo.user_id == user_id
    )

    if search:
        query = query.filter(
            models.Todo.title.contains(search)
        )

    return query.order_by(
        models.Todo.id.desc()
    ).all()


def get_user_by_email(db, email):

    return db.query(models.User).filter(
        models.User.email == email
    ).first()

def get_user_statistics(
    db: Session,
    user_id: int
):

    tasks = db.query(models.Todo).filter(
        models.Todo.user_id == user_id
    ).all()

    total = len(tasks)

    completed = len(
        [task for task in tasks if task.completed]
    )

    pending = total - completed

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }


def update_user(
    db: Session,
    user_id: int,
    user_data
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        return None

    user.username = user_data.username
    user.email = user_data.email

    db.commit()

    db.refresh(user)

    return user


def update_password(
    db: Session,
    user_id: int,
    new_password: str
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        return None

    user.password = hash_password(new_password)

    db.commit()

    db.refresh(user)

    return user