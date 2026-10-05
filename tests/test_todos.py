import time
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_get_todos():
    response = client.get("/api/todos")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_todo():
    response = client.post(
        "/api/todos",
        json={
            "title": "Test Todo"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    assert "id" in data    

def test_update_todo():
    create_response = client.post(
        "/api/todos",
        json={
            "title": "Todo Before Update"
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    update_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "title": "Todo After Update",
            "completed": True
        }
    )

    assert update_response.status_code == 200

    updated_todo = update_response.json()

    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Todo After Update"
    assert updated_todo["completed"] is True

def test_delete_todo():
    create_response = client.post(
        "/api/todos",
        json={
            "title": "Todo To Delete"
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    delete_response = client.delete(
        f"/api/todos/{todo_id}"
    )

    assert delete_response.status_code == 200

    delete_data = delete_response.json()

    assert delete_data["message"] == "Todo deleted successfully"
    assert delete_data["deleted_todo"]["id"] == todo_id

    get_response = client.get(
        f"/api/todos"
    )

    assert get_response.status_code == 200

    todos = get_response.json()

    assert all(todo["id"] != todo_id for todo in todos)

def test_update_nonexistent_todo():
    response = client.put(
        "/api/todos/999999",
        json={
            "title": "This Todo Does Not Exist"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Todo not found"

def test_delete_nonexistent_todo():
    response = client.delete(
        "/api/todos/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Todo not found"

def test_create_todo_with_empty_title():
    response = client.post(
        "/api/todos",
        json={
            "title": ""
        }
    )

    assert response.status_code == 422   

def test_toggle_todo_completed():
    create_response = client.post(
        "/api/todos",
        json={
            "title": "Todo To Complete"
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    assert created_todo["completed"] is False

    complete_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "completed": True
        }
    )

    assert complete_response.status_code == 200

    completed_todo = complete_response.json()

    assert completed_todo["completed"] is True
    assert completed_todo["title"] == "Todo To Complete"

    uncomplete_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "completed": False
        }
    )

    assert uncomplete_response.status_code == 200

    uncompleted_todo = uncomplete_response.json()

    assert uncompleted_todo["completed"] is False
    assert uncompleted_todo["title"] == "Todo To Complete"     

def test_completed_and_pending_todos():
    todo_ids = []

    for title in ["Completed Task 1", "Pending Task", "Completed Task 2"]:
        response = client.post(
            "/api/todos",
            json={
                "title": title
            }
        )

        assert response.status_code == 200

        todo_ids.append(response.json()["id"])

    first_complete_response = client.put(
        f"/api/todos/{todo_ids[0]}",
        json={
            "completed": True
        }
    )

    assert first_complete_response.status_code == 200

    second_complete_response = client.put(
        f"/api/todos/{todo_ids[2]}",
        json={
            "completed": True
        }
    )

    assert second_complete_response.status_code == 200

    response = client.get("/api/todos")

    assert response.status_code == 200

    todos = response.json()

    test_todos = [
        todo
        for todo in todos
        if todo["id"] in todo_ids
    ]

    completed_count = sum(
        1 for todo in test_todos
        if todo["completed"] is True
    )

    pending_count = sum(
        1 for todo in test_todos
        if todo["completed"] is False
    )

    assert completed_count == 2
    assert pending_count == 1

def test_edit_title_without_changing_completed_status():
    create_response = client.post(
        "/api/todos",
        json={
            "title": "Original Task"
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    assert created_todo["completed"] is False

    update_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "title": "Edited Task"
        }
    )

    assert update_response.status_code == 200

    updated_todo = update_response.json()

    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Edited Task"
    assert updated_todo["completed"] is False

def test_toggle_completed_without_changing_title():
    create_response = client.post(
        "/api/todos",
        json={
            "title": "Important Task"
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()
    todo_id = created_todo["id"]

    assert created_todo["title"] == "Important Task"
    assert created_todo["completed"] is False

    complete_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "completed": True
        }
    )

    assert complete_response.status_code == 200

    completed_todo = complete_response.json()

    assert completed_todo["completed"] is True
    assert completed_todo["title"] == "Important Task"

def test_todo_persists_in_database():
    title = "Persistent Database Todo"

    create_response = client.post(
        "/api/todos",
        json={
            "title": title
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()

    todo_id = created_todo["id"]

    assert created_todo["title"] == title

    get_response = client.get("/api/todos")

    assert get_response.status_code == 200

    todos = get_response.json()

    matching_todos = [
        todo
        for todo in todos
        if todo["id"] == todo_id
    ]

    assert len(matching_todos) == 1

    persisted_todo = matching_todos[0]

    assert persisted_todo["id"] == todo_id
    assert persisted_todo["title"] == title
    assert persisted_todo["completed"] is False

def test_todo_has_timestamps():
    response = client.post(
        "/api/todos",
        json={
            "title": "Timestamp Todo"
        }
    )

    assert response.status_code == 200

    todo = response.json()

    assert "created_at" in todo
    assert "updated_at" in todo

    assert todo["created_at"] is not None
    assert todo["updated_at"] is not None    

def test_updated_at_changes_when_todo_is_updated():
    create_response = client.post(
        "/api/todos",
        json={
            "title": "Timestamp Update Test"
        }
    )

    assert create_response.status_code == 200

    created_todo = create_response.json()

    todo_id = created_todo["id"]
    original_created_at = created_todo["created_at"]
    original_updated_at = created_todo["updated_at"]

    assert original_created_at is not None
    assert original_updated_at is not None
    time.sleep(1.1)
    update_response = client.put(
        f"/api/todos/{todo_id}",
        json={
            "title": "Updated Timestamp Test"
        }
    )

    assert update_response.status_code == 200

    updated_todo = update_response.json()

    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Updated Timestamp Test"

    assert updated_todo["created_at"] == original_created_at
    assert updated_todo["updated_at"] != original_updated_at

def test_create_todo_without_title():
    response = client.post(
        "/api/todos",
        json={}
    )

    assert response.status_code == 422

def test_create_todo_with_invalid_title_type():
    response = client.post(
        "/api/todos",
        json={
            "title": 123
        }
    )

    assert response.status_code == 422 

def test_create_todo_with_empty_title():
    response = client.post(
        "/api/todos",
        json={
            "title": ""
        }
    )

    assert response.status_code == 422

def test_create_todo_with_whitespace_only_title():
    response = client.post(
        "/api/todos",
        json={
            "title": "     "
        }
    )

    assert response.status_code == 422              