import json
from datetime import datetime
from base.project_board_base import ProjectBoardBase
from storage.file_storage import FileStorage
from constants.paths import BOARDS_DB,TASKS_DB


class BoardService(ProjectBoardBase):

    # -------------------------
    # CREATE BOARD
    # -------------------------
    def create_board(self, request: str):

        data = json.loads(request)

        name = data["name"]
        description = data["description"]
        team_id = data["team_id"]
        creation_time = data["creation_time"]

        if len(name) > 64:
            raise Exception("Board name too long")

        if len(description) > 128:
            raise Exception("Description too long")

        boards = FileStorage.read(BOARDS_DB)

        for b in boards:
            if b["team_id"] == team_id and b["name"] == name:
                raise Exception("Board name must be unique per team")

        board_id = str(len(boards) + 1)

        board = {
            "id": board_id,
            "name": name,
            "description": description,
            "team_id": team_id,
            "status": "OPEN",
            "creation_time": creation_time,
            "end_time": None
        }

        boards.append(board)

        FileStorage.write(BOARDS_DB, boards)

        return json.dumps({"id": board_id})

    # -------------------------
    # CLOSE BOARD
    # -------------------------
    def close_board(self, request: str):

        data = json.loads(request)

        board_id = data["id"]

        boards = FileStorage.read(BOARDS_DB)
        tasks = FileStorage.read(TASKS_DB)

        for b in boards:

            if b["id"] == board_id:

                # check tasks completed
                for t in tasks:
                    if t["board_id"] == board_id and t["status"] != "COMPLETE":
                        raise Exception("All tasks must be COMPLETE")

                b["status"] = "CLOSED"
                b["end_time"] = str(datetime.now())

                FileStorage.write(BOARDS_DB, boards)

                return json.dumps({"status": "success"})

        raise Exception("Board not found")

    # -------------------------
    # ADD TASK
    # -------------------------
    def add_task(self, request: str):

        data = json.loads(request)

        title = data["title"]
        description = data["description"]
        user_id = data["user_id"]
        creation_time = data["creation_time"]
        board_id = data["board_id"]

        if len(title) > 64:
            raise Exception("Task title too long")

        if len(description) > 128:
            raise Exception("Description too long")

        boards = FileStorage.read(BOARDS_DB)

        board_found = False

        for b in boards:

            if b["id"] == board_id:

                board_found = True

                if b["status"] != "OPEN":
                    raise Exception("Cannot add task to CLOSED board")

        if not board_found:
            raise Exception("Board not found")

        tasks = FileStorage.read(TASKS_DB)

        for t in tasks:
            if t["board_id"] == board_id and t["title"] == title:
                raise Exception("Task title must be unique per board")

        task_id = str(len(tasks) + 1)

        task = {
            "id": task_id,
            "board_id": board_id,
            "title": title,
            "description": description,
            "user_id": user_id,
            "status": "OPEN",
            "creation_time": creation_time
        }

        tasks.append(task)

        FileStorage.write(TASKS_DB, tasks)

        return json.dumps({"id": task_id})

    # -------------------------
    # UPDATE TASK STATUS
    # -------------------------
    def update_task_status(self, request: str):

        data = json.loads(request)

        task_id = data["id"]
        status = data["status"]

        if status not in ["OPEN", "IN_PROGRESS", "COMPLETE"]:
            raise Exception("Invalid status")

        tasks = FileStorage.read(TASKS_DB)

        for t in tasks:

            if t["id"] == task_id:

                t["status"] = status

                FileStorage.write(TASKS_DB, tasks)

                return json.dumps({"status": "success"})

        raise Exception("Task not found")

    # -------------------------
    # LIST BOARDS
    # -------------------------
    def list_boards(self, request: str):

        data = json.loads(request)

        team_id = data["id"]

        boards = FileStorage.read(BOARDS_DB)

        result = []

        for b in boards:

            if b["team_id"] == team_id and b["status"] == "OPEN":

                result.append({
                    "id": b["id"],
                    "name": b["name"]
                })

        return json.dumps(result)

    # -------------------------
    # EXPORT BOARD
    # -------------------------
    def export_board(self, request: str):

        data = json.loads(request)

        board_id = data["id"]

        boards = FileStorage.read(BOARDS_DB)
        tasks = FileStorage.read(TASKS_DB)

        board = None

        for b in boards:
            if b["id"] == board_id:
                board = b

        if board is None:
            raise Exception("Board not found")

        file_name = f"out/board_{board_id}.txt"

        with open(file_name, "w") as f:

            f.write(f"Board: {board['name']}\n")
            f.write(f"Description: {board['description']}\n")
            f.write(f"Status: {board['status']}\n\n")

            f.write("Tasks:\n")

            for t in tasks:
                if t["board_id"] == board_id:

                    f.write(
                        f"- {t['title']} | Status: {t['status']} | Assigned To: {t['user_id']}\n"
                    )

        return json.dumps({"out_file": file_name})