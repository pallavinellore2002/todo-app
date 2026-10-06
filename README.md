# Todo App

A full-stack Todo application built with a Python FastAPI backend, MySQL database, and HTML/CSS/JavaScript frontend.

The application allows users to create, view, edit, complete, and delete Todo items.

---

## Features

- Create a Todo
- View all Todos
- Edit Todo title
- Mark Todo as completed
- Mark completed Todo as pending
- Delete Todo
- Completed and pending Todo counts
- MySQL database persistence
- REST API using FastAPI
- Input validation using Pydantic
- Automated API tests using pytest
- Environment-based database configuration
- Git version control

---

## Technology Stack

### Backend

- Python 3.10.11
- FastAPI
- Uvicorn
- Pydantic
- mysql-connector-python
- python-dotenv

### Frontend

- HTML
- CSS
- JavaScript

### Database

- MySQL 8.0

### Testing

- pytest
- FastAPI TestClient
- httpx

### Version Control

- Git
- GitHub

---

## Project Structure

```text
todo-app/
│
├── backend/
│   ├── __init__.py
│   ├── database.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── database/
│   └── schema.sql
│
├── tests/
│   └── test_todos.py
│
├── .env
├── .gitignore
├── API.md
├── ENTITY.md
├── REQUIREMENTS.md
├── pytest.ini
└── README.md