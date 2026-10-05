from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from backend.database import get_connection
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class TodoCreate(BaseModel):
    title: str = Field(min_length=1)
    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace only")

        return value

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

@app.get("/")
def home():
    return {"message": "Todo API is running"}

@app.get("/api/todos")
def get_todos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, title, completed, created_at, updated_at
        FROM todos
        ORDER BY id ASC
    """)
    todos = cursor.fetchall()
    for todo in todos:
        todo["completed"] = bool(todo["completed"])
    cursor.close()
    connection.close()
    return todos

@app.post("/api/todos")
def create_todo(todo: TodoCreate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        INSERT INTO todos (title)
        VALUES (%s)
        """,
        (todo.title,)
    )
    connection.commit()
    todo_id = cursor.lastrowid
    cursor.execute(
        """
        SELECT id, title, completed, created_at, updated_at
        FROM todos
        WHERE id = %s
        """,
        (todo_id,)
    )
    created_todo = cursor.fetchone()
    created_todo["completed"] = bool(created_todo["completed"])
    cursor.close()
    connection.close()
    return created_todo

@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, title, completed, created_at, updated_at
        FROM todos
        WHERE id = %s
        """,
        (todo_id,)
    )

    existing_todo = cursor.fetchone()

    if existing_todo is None:
        cursor.close()
        connection.close()
        raise HTTPException(
        status_code=404,
        detail="Todo not found"
        )

    new_title = (
        todo.title
        if todo.title is not None
        else existing_todo["title"]
    )

    new_completed = (
        todo.completed
        if todo.completed is not None
        else existing_todo["completed"]
    )

    cursor.execute(
        """
        UPDATE todos
        SET title = %s,
            completed = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (new_title, new_completed, todo_id)
    )

    connection.commit()

    cursor.execute(
        """
        SELECT id, title, completed, created_at, updated_at
        FROM todos
        WHERE id = %s
        """,
        (todo_id,)
    )

    updated_todo = cursor.fetchone()
    updated_todo["completed"] = bool(updated_todo["completed"])

    cursor.close()
    connection.close()

    return updated_todo

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, title, completed, created_at, updated_at
        FROM todos
        WHERE id = %s
        """,
        (todo_id,)
    )

    existing_todo = cursor.fetchone()

    if existing_todo is None:
        cursor.close()
        connection.close()
        raise HTTPException(
        status_code=404,
        detail="Todo not found"
        )

    cursor.execute(
        """
        DELETE FROM todos
        WHERE id = %s
        """,
        (todo_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Todo deleted successfully",
        "deleted_todo": existing_todo
    }