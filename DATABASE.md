# Todo App Database Guide

This project stores todos in **MySQL**. The FastAPI backend connects using `backend/database.py`; the API reads and writes a table named `todos` in the database selected by the `DB_NAME` environment variable.

> **Schema note:** There is no database creation or migration script in the project. The SQL below is a setup template derived from `ENTITY.md` and the queries in `backend/main.py`. Create the database/table before using the API, and keep the actual schema aligned with this template.

## 1. Requirements

- A running MySQL server accessible from the machine running the backend.
- A MySQL database and a `todos` table with the columns listed below.
- Python dependencies installed from the project's dependency setup, including `mysql-connector-python` and `python-dotenv`.

## 2. Create the database and table

The following example names the database `todo_app`. If you choose another name, use that same name for `DB_NAME` in `.env`.

```sql
CREATE DATABASE IF NOT EXISTS todo_app
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE todo_app;

CREATE TABLE IF NOT EXISTS todos (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

The API inserts only the todo title on creation, so the database must supply the default for `completed`, `created_at`, and `updated_at`. When a todo is edited, the API explicitly sets `updated_at = CURRENT_TIMESTAMP` and leaves `created_at` unchanged.

## 3. Configure the database connection

`backend/database.py` calls `load_dotenv()` and reads these variables from the environment (normally from a `.env` file in the project root):

```dotenv
DB_HOST=127.0.0.1
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=todo_app
```

Use the host, user, password, and database name for your own MySQL installation. The current code does not read a `DB_PORT` variable; MySQL Connector/Python therefore uses its default port unless the code is changed to configure another one.

Keep real credentials private. Do not paste passwords into source files or commit a populated `.env` file to a shared repository.

## 4. Todo table reference

| Column | MySQL type | Required | Default / behavior |
|---|---|---|---|
| `id` | `INT` | Yes | Auto-incrementing primary key. |
| `title` | `VARCHAR(255)` | Yes | Supplied by the user/API. The entity rules say it must not be empty or whitespace-only. |
| `completed` | `BOOLEAN` | Yes | `FALSE` for newly created todos. MySQL stores `BOOLEAN` as a tiny integer type. |
| `created_at` | `DATETIME` | Yes | Set to the current timestamp when inserted; the API does not change it during updates. |
| `updated_at` | `DATETIME` | Yes | Set on insert and explicitly refreshed by the API on update. |

There are no relationships to other tables in the current Todo entity.

## 5. How the backend uses MySQL

The connection helper builds its configuration from `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`. Each API route obtains a connection, performs its SQL operation, and closes the cursor and connection.

- **Create:** inserts a row with `title`, commits, then reads the inserted row to return it.
- **List:** selects the Todo fields and orders results by `id` ascending.
- **Update:** first looks up the row; if found, updates the title/completion values and sets `updated_at` to the current timestamp, then returns the updated row.
- **Delete:** looks up the row, deletes it, commits, and returns the deleted row in the API response.

The API returns `404` when update or delete cannot find the requested todo. The backend does not currently define a custom response for database connection or query failures.

## 6. Verify the connection

From the project root, with the project's Python environment active and `.env` configured, run:

```bash
python -m backend.database
```

On success, the script prints:

```text
MySQL connection successful!
```

This verifies that the configured server and database can be reached. It does **not** verify that the `todos` table has the right columns; check the table schema separately if API queries fail.

## 7. Testing database guidance

The API tests use the database configured for the application. Several tests create todo rows, and the test file does not clean up every created row. Point tests at a separate test database rather than a database containing important personal or production data. Ensure the test database has the same `todos` schema before running the suite.

## 8. Common problems

- **Connection refused / server unavailable:** Confirm MySQL is running and `DB_HOST` points to a reachable host.
- **Access denied:** Check `DB_USER` and `DB_PASSWORD`, and confirm that user has access to the selected database.
- **Unknown database:** Create the database or correct `DB_NAME` in `.env`.
- **Table doesn't exist:** Run the `CREATE TABLE` statement above against the configured database.
- **Unknown column / SQL error:** Compare the live `todos` table with the five-column schema in this guide. The API expects `id`, `title`, `completed`, `created_at`, and `updated_at`.
- **Changes do not appear:** Confirm the backend is using the database you intended; check `DB_NAME` and verify the row directly in MySQL.

## 9. Data and operational notes

- Todos are persisted in MySQL and remain there until deleted; deleting a todo through the API removes its row.
- Back up the database using the backup process appropriate for your MySQL installation before making schema or data changes.
- Do not use the development/test database for production data without appropriate access control, backups, and deployment configuration.
