# Team Project Planner

## Overview

This project implements a **Team Project Planner Tool** using Python.
The system provides APIs to manage:

* Users
* Teams
* Project Boards
* Tasks within Boards

The APIs follow the contracts defined in the provided base classes.
Each API accepts **JSON strings as input** and returns **JSON strings as output**.

Instead of using a database, the system uses **local JSON files for persistence**.

---

# Architecture

The project follows a simple layered architecture:

```
Base Layer → API Contracts
Service Layer → Business Logic
Storage Layer → File Persistence
Constants Layer → Configuration
```

### Base Layer

Defines the API contracts provided in the assignment.

```
base/
    user_base.py
    team_base.py
    project_board_base.py
```

---

### Service Layer

Implements all business logic for the APIs.

```
services/
    user_service.py
    team_service.py
    board_service.py
```

Responsibilities include:

* Parsing input JSON
* Validating constraints
* Managing relationships between entities
* Updating persistent storage

---

### Storage Layer

Handles file-based persistence.

```
storage/
    file_storage.py
```

Example usage:

```
FileStorage.read("db/users.json")
FileStorage.write("db/users.json", data)
```

This centralizes file operations and prevents duplication across services.

---

### Constants Layer

Contains centralized configuration values such as file paths.

```
constants/
    paths.py
```

---

# Project Structure

```
factwise-python/

base/
    user_base.py
    team_base.py
    project_board_base.py

services/
    user_service.py
    team_service.py
    board_service.py

storage/
    file_storage.py

constants/
    paths.py

db/
    users.json
    teams.json
    boards.json
    tasks.json

out/
    (generated board export files)

main.py
README.md
requirements.txt
ProblemStatement.md
```

---

# Data Persistence

The application stores all data in JSON files inside the **db/** folder.

| File        | Purpose                          |
| ----------- | -------------------------------- |
| users.json  | Stores user information          |
| teams.json  | Stores teams and team members    |
| boards.json | Stores project boards            |
| tasks.json  | Stores tasks belonging to boards |

Example user record:

```
{
  "id": "1",
  "name": "amit",
  "display_name": "Amit Pandey",
  "creation_time": "2026-03-10"
}
```

**Important**

The `db` folder contains initial JSON files used for persistence.
Each file is initialized with an empty array.

Example:

```
[]
```

This ensures the application can run without requiring the user to create database files manually.

---

# API Modules

## User APIs

Manages users in the system.

Implemented methods:

* `create_user`
* `list_users`
* `describe_user`
* `update_user`
* `get_user_teams`

Example request:

```
{
  "name": "amit",
  "display_name": "Amit Pandey"
}
```

Example response:

```
{
  "id": "1"
}
```

---

## Team APIs

Manages teams and team membership.

Implemented methods:

* `create_team`
* `list_teams`
* `describe_team`
* `update_team`
* `add_users_to_team`
* `remove_users_from_team`
* `list_team_users`

Example request:

```
{
  "name": "Backend Team",
  "description": "API Development",
  "admin": "1"
}
```

---

## Project Board APIs

Manages boards and tasks within boards.

Implemented methods:

* `create_board`
* `close_board`
* `add_task`
* `update_task_status`
* `list_boards`
* `export_board`

Example request:

```
{
  "name": "Sprint 1",
  "description": "Login feature",
  "team_id": "1",
  "creation_time": "2026-03-10"
}
```

---

# Board Export

The `export_board` API exports board details and tasks to a text file.

Example output file:

```
out/board_1.txt
```

Example content:

```
Board: Sprint 1
Description: Login feature

Tasks:
- Login API | Status: COMPLETE | Assigned To: 1
```

---

# Running the Project

Navigate to the project directory:

```
cd factwise-python
```

Run the main script:

```
python main.py
```

The `main.py` file can be used to test the APIs.

---

# Design Decisions

### JSON-based Storage

JSON files were used instead of a database to satisfy the assignment requirement of **local file persistence**.

### Layered Architecture

Separating the project into base, service, storage, and constants layers improves code organization and maintainability.

### Centralized File Operations

The `FileStorage` utility ensures all file operations are handled in one place.

---

# Assumptions

* IDs are generated as sequential string values.
* A user can belong to multiple teams.
* Each team has one admin.
* Boards belong to a single team.
* Tasks belong to a single board.
* A board can only be closed when all tasks are marked as `COMPLETE`.

---

# Dependencies

The project uses only the **Python standard library**, so no additional dependencies are required.
