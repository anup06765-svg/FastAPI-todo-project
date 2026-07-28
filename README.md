# 🚀 FastAPI Todo Management System

A modern **Todo Management System** built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Jinja2 Templates**. The application allows users to register, log in securely, and manage their personal tasks with features like task priorities, categories, due dates, search, profile management, and task statistics.

---

# 📌 Features

* 🔐 User Registration
* 🔑 Secure User Login & Logout
* 🔒 Password Hashing
* 👤 User Profile Management
* 🔄 Change Password
* ✅ Create Todo
* 📝 Update Todo
* ❌ Delete Todo
* ✔️ Mark Task as Completed
* 🔍 Search Tasks
* 📂 Task Categories
* 🚩 Task Priority (Low, Medium, High)
* 📅 Due Date Support
* 📊 User Task Statistics
* 💾 SQLite Database
* ⚡ FastAPI Backend
* 🎨 Jinja2 HTML Templates
* 🗂️ SQLAlchemy ORM

---

# 🛠 Tech Stack

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Jinja2
* Uvicorn
* Starlette Sessions

---

# 📂 Project Structure

```text
Todo-App/
│
├── app/
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│
├── static/
├── templates/
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/fastapi-todo.git
```

```bash
cd fastapi-todo
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn main:app --reload
```

Open your browser and visit:

```text
http://127.0.0.1:8000
```

---

# 📋 Functionalities

### Authentication

* Register User
* Login
* Logout
* Session Management
* Password Encryption

### Todo Management

* Create Task
* Edit Task
* Delete Task
* Complete Task
* Search Tasks
* Filter by User

### User Profile

* View Profile
* Edit Profile
* Change Password
* View Task Statistics

---

# 🗄 Database

The project uses **SQLite** as the database.

Tables:

* users
* todos

Relationship:

* One User → Many Todos

---

# 📊 User Dashboard

Each user can view:

* Total Tasks
* Completed Tasks
* Pending Tasks

---

# 🔐 Security

* Password Hashing
* Session Authentication
* User-specific Todo Access
* Protected Routes

---

# 📦 Dependencies

* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* Jinja2
* Starlette
* Typing Extensions

---

# 🚀 Future Improvements

* JWT Authentication
* Email Verification
* Password Reset
* REST API Documentation
* Docker Support
* PostgreSQL Support
* Redis Cache
* Unit Testing
* Pagination
* Dark Mode
* Docker Deployment
* CI/CD Pipeline

---

# 👨‍💻 Author

**Anup Kumar**

Python Developer | FastAPI Developer | Backend Developer

GitHub:
https://github.com/anup06765-svg

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
