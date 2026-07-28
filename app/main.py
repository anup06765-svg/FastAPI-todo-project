from fastapi import FastAPI,Request, Depends, Form,HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models, crud, schemas
from app.auth import verify_password
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="mysecretkey123"
)

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#@app.get("/")
#def home(request: Request):

    #return templates.TemplateResponse(
        #request=request,
        #name="index.html",)

from fastapi import Query

@app.get("/")
def home(
    request: Request,
    search: str = Query(default=""),
    db: Session = Depends(get_db)
):

    if "user" not in request.session:
        print("Session Not Found")
        return RedirectResponse(
            "/register",
            status_code=303
        )

    username = request.session["user"]
    print("Username =", username)

    user = crud.get_user_by_username(
    db,
    username
    )
    print("User =", user)

# Agar session me user hai lekin database me nahi mila
    if user is None:
        print("User is None")
        request.session.clear()
        return RedirectResponse(
            "/login",
            status_code=303
        )

    tasks = crud.search_tasks_by_user(
        db,
        user.id,
        search
    )

    total = len(tasks)
    completed = len([t for t in tasks if t.completed])
    pending = total - completed

    response = templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "tasks": tasks,
        "username": username,
        "total": total,
        "completed": completed,
        "pending": pending,
        "search": search
    }
)

    response.headers["Cache-Control"] = "no-store"

    return response

@app.post("/add")
def add_task(

    request: Request,

    title: str = Form(...),

    priority: str = Form(...),

    category: str = Form(...),

    due_date: str = Form(...),

    db: Session = Depends(get_db)

):

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    todo = schemas.TodoCreate(

        title=title,

        priority=priority,

        category=category,

        due_date=due_date

    )

    crud.create_task(

        db,

        todo,

        user.id

    )

    return RedirectResponse(
        "/",
        status_code=303
    )

@app.get("/delete/{task_id}")
def delete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    crud.delete_task(
        db,
        task_id,
        user.id
    )

    return RedirectResponse(
        "/",
        status_code=303
    )


@app.get("/complete/{task_id}")
def complete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    crud.toggle_complete(
        db,
        task_id,
        user.id
    )

    return RedirectResponse(
        "/",
        status_code=303
    )

@app.get("/edit/{task_id}")
def edit_page(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    task = crud.get_task_by_user(
        db,
        task_id,
        user.id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="edit_task.html",
        context={
            "task": task
        }
    )

@app.post("/update/{task_id}")
def update_task(

    task_id: int,

    request: Request,

    title: str = Form(...),

    completed: bool = Form(False),

    priority: str = Form(...),

    category: str = Form(...),

    due_date: str = Form(...),

    db: Session = Depends(get_db)

):

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    todo = schemas.TodoUpdate(

        title=title,

        completed=completed,

        priority=priority,

        category=category,

        due_date=due_date

    )

    task = crud.update_task(
        db,
        task_id,
        user.id,
        todo
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return RedirectResponse(
        "/",
        status_code=303
    )


@app.get("/register")
def register_page(request: Request):

    # Agar user already login hai
    if "user" in request.session:
        return RedirectResponse(
            "/",
            status_code=303
        )

    response = templates.TemplateResponse(
        request=request,
        name="register.html"
    )

    # Browser cache disable
    response.headers["Cache-Control"] = "no-store"

    return response



@app.post("/register")
def register(

    request: Request,

    username: str = Form(...),

    email: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)

):

    user = schemas.UserCreate(

        username=username,

        email=email,

        password=password

    )
    print("1. Register Started")
    if crud.get_user_by_username(db, username):
        print("2. Username Exists")
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Username already exists"
        }
    )
    print("3. Username OK")
    if crud.get_user_by_email(db, email):
        print("4. Email Exists")
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Email already exists"
        }
    )
    print("5. Email OK")
    new_user = crud.create_user(
    db,
    user
    )
    print("6. User Created")
    request.session["user"] = new_user.username
    print("7. Session Created")
    return RedirectResponse(
        "/",
        status_code=303
    )

@app.get("/login")
def login_page(request: Request):

    # Agar user already login hai
    if "user" in request.session:
        return RedirectResponse(
            "/",
            status_code=303
        )

    response = templates.TemplateResponse(
        request=request,
        name="login.html"
    )

    # Browser cache disable
    response.headers["Cache-Control"] = "no-store"

    return response


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_username(db, username)

    if user is None:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Username not found"
            }
    )

    if not verify_password(password, user.password):

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Incorrect password"
            }
    )

    request.session["user"] = user.username
    print("Session =", request.session)
    return RedirectResponse("/", status_code=303)

@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        "/login",
        status_code=303
    )

@app.get("/users")
def users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    for u in users:
        print(u.id, u.username, u.email)

    return users

@app.get("/profile")
def profile_page(
    request: Request,
    db: Session = Depends(get_db)
):

    if "user" not in request.session:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    stats = crud.get_user_statistics(
        db,
        user.id
    )

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user,
            "stats": stats
        }
    )

@app.get("/profile/edit")
def edit_profile_page(
    request: Request,
    db: Session = Depends(get_db)
):

    if "user" not in request.session:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    return templates.TemplateResponse(
        request=request,
        name="edit_profile.html",
        context={
            "user": user
        }
    )


@app.post("/profile/edit")
def update_profile(

    request: Request,

    username: str = Form(...),

    email: str = Form(...),

    db: Session = Depends(get_db)

):

    current_username = request.session["user"]

    current_user = crud.get_user_by_username(
        db,
        current_username
    )

    existing_user = crud.get_user_by_username(
        db,
        username
    )

    if existing_user and existing_user.id != current_user.id:

        return templates.TemplateResponse(
            request=request,
            name="edit_profile.html",
            context={
                "user": current_user,
                "error": "Username already exists."
            }
        )

    existing_email = crud.get_user_by_email(
        db,
        email
    )

    if existing_email and existing_email.id != current_user.id:

        return templates.TemplateResponse(
            request=request,
            name="edit_profile.html",
            context={
                "user": current_user,
                "error": "Email already exists."
            }
        )

    user_data = schemas.UserUpdate(

        username=username,

        email=email

    )

    crud.update_user(
        db,
        current_user.id,
        user_data
    )

    request.session["user"] = username

    return RedirectResponse(
        "/profile",
        status_code=303
    )


@app.get("/profile/password")
def change_password_page(
    request: Request,
    db: Session = Depends(get_db)
):

    if "user" not in request.session:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="change_password.html"
    )

@app.post("/profile/password")
def change_password(

    request: Request,

    current_password: str = Form(...),

    new_password: str = Form(...),

    confirm_password: str = Form(...),

    db: Session = Depends(get_db)

):

    username = request.session["user"]

    user = crud.get_user_by_username(
        db,
        username
    )

    if not verify_password(
        current_password,
        user.password
    ):

        return templates.TemplateResponse(
            request=request,
            name="change_password.html",
            context={
                "error": "Current password is incorrect."
            }
        )

    if new_password != confirm_password:

        return templates.TemplateResponse(
            request=request,
            name="change_password.html",
            context={
                "error": "New passwords do not match."
            }
        )

    crud.update_password(
        db,
        user.id,
        new_password
    )

    return templates.TemplateResponse(
        request=request,
        name="change_password.html",
        context={
            "success": "Password changed successfully."
        }
    )