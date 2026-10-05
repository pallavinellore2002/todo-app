# Todo App Requirements

## 1. Create a Todo

### User Story
As a user, I want to create a todo so that I can keep track of a task I need to complete.

### Expected Behavior
- The user enters a todo title.
- The system creates the todo.
- The system assigns a unique ID.
- The system sets `completed` to `false` by default.
- The system generates `created_at` and `updated_at`.
- The newly created todo is stored in MySQL.

### Failure Cases
- The title is missing.
- The title is empty.
- The title contains only whitespace.
- The title is not a string.
- The database is unavailable.

---

## 2. View All Todos

### User Story
As a user, I want to see all my todos so that I can know which tasks I need to complete.

### Expected Behavior
- The system returns all todos.
- Each todo contains:
  - `id`
  - `title`
  - `completed`
  - `created_at`
  - `updated_at`
- Todos are returned in a predictable order.

### Failure Cases
- The database is unavailable.
- A database query fails.

---

## 3. Edit a Todo

### User Story
As a user, I want to edit a todo so that I can correct or update a task.

### Expected Behavior
- The user can update the title.
- The user can update the completed status.
- Updating the title should not unexpectedly change the completed status.
- Updating the completed status should not unexpectedly change the title.
- `updated_at` changes when the todo is updated.
- `created_at` remains unchanged.

### Failure Cases
- The todo does not exist.
- The title is invalid.
- The completed value is not a boolean.
- The database is unavailable.

---

## 4. Mark a Todo as Done

### User Story
As a user, I want to mark a todo as completed so that I know the task has been finished.

### Expected Behavior
- The user can change `completed` from `false` to `true`.
- The user can change `completed` from `true` to `false`.
- The title remains unchanged when only the completed status is changed.
- `updated_at` changes when the status changes.

### Failure Cases
- The todo does not exist.
- The completed value is not a boolean.
- The database is unavailable.

---

## 5. Delete a Todo

### User Story
As a user, I want to delete a todo so that I can remove a task I no longer need.

### Expected Behavior
- The selected todo is removed from the database.
- The deleted todo no longer appears when todos are retrieved.
- The user receives confirmation that the todo was deleted.

### Failure Cases
- The todo does not exist.
- The database is unavailable.