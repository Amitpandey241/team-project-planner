import json
import uuid
from datetime import datetime
from base.user_base import UserBase
from constants.paths import USERS_DB,TEAMS_DB



class UserService(UserBase):

    # READ IN JSON FILE
    def _read_file(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    # WRITE IN JSON FILE
    def _write_file(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    # CREATE USER
    def create_user(self, request: str) -> str:

        data = json.loads(request)

        name = data.get("name")
        display_name = data.get("display_name")

        if not name or not display_name:
            raise Exception("Invalid input")

        if len(name) > 64:
            raise Exception("Name cannot exceed 64 characters")

        if len(display_name) > 64:
            raise Exception("Display name cannot exceed 64 characters")

        users = self._read_file(USERS_DB)

        # check uniqueness
        for u in users:
            if u["name"] == name:
                raise Exception("User name must be unique")

        user_id = str(len(users) + 1)

        user = {
            "id": user_id,
            "name": name,
            "display_name": display_name,
            "creation_time": str(datetime.now())
        }

        users.append(user)

        self._write_file(USERS_DB, users)

        return json.dumps({"id": user_id})

   
    # LIST USERS
    def list_users(self) -> str:

        users = self._read_file(USERS_DB)

        result = []

        for u in users:
            result.append({
                "name": u["name"],
                "display_name": u["display_name"],
                "creation_time": u["creation_time"]
            })

        return json.dumps(result)

    # DESCRIBE USER
    def describe_user(self, request: str) -> str:

        data = json.loads(request)
        user_id = data.get("id")

        users = self._read_file(USERS_DB)

        for u in users:
            if u["id"] == user_id:
                response = {
                    "name": u["name"],
                    "description": u["display_name"],
                    "creation_time": u["creation_time"]
                }
                return json.dumps(response)

        raise Exception("User not found")

    # UPDATE USER
    def update_user(self, request: str) -> str:

        data = json.loads(request)

        user_id = data.get("id")
        user_data = data.get("user")

        users = self._read_file(USERS_DB)

        for u in users:

            if u["id"] == user_id:

                # username cannot change
                if user_data["name"] != u["name"]:
                    raise Exception("User name cannot be updated")

                if len(user_data["display_name"]) > 128:
                    raise Exception("Display name too long")

                u["display_name"] = user_data["display_name"]

                self._write_file(USERS_DB, users)

                return json.dumps({"status": "success"})

        raise Exception("User not found")

    # GET USER TEAMS
    def get_user_teams(self, request: str) -> str:

        data = json.loads(request)

        user_id = data.get("id")

        teams = self._read_file(TEAMS_DB)

        result = []

        for t in teams:

            if "users" in t and user_id in t["users"]:

                result.append({
                    "name": t["name"],
                    "description": t["description"],
                    "creation_time": t["creation_time"]
                })

        return json.dumps(result)