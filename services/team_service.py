import json
from datetime import datetime
from base.team_base import TeamBase
from storage.file_storage import FileStorage
from constants.paths import USERS_DB,TEAMS_DB


class TeamService(TeamBase):

    # CREATE TEAM
    def create_team(self, request: str) -> str:

        data = json.loads(request)

        name = data["name"]
        description = data["description"]
        admin = data["admin"]

        if len(name) > 64:
            raise Exception("Team name too long")

        if len(description) > 128:
            raise Exception("Description too long")

        teams = FileStorage.read(TEAMS_DB)

        # check unique name
        for t in teams:
            if t["name"] == name:
                raise Exception("Team name must be unique")

        team_id = str(len(teams) + 1)

        team = {
            "id": team_id,
            "name": name,
            "description": description,
            "admin": admin,
            "users": [admin],
            "creation_time": str(datetime.now())
        }

        teams.append(team)

        FileStorage.write(TEAMS_DB, teams)

        return json.dumps({"id": team_id})

    # LIST TEAMS
    def list_teams(self) -> str:

        teams = FileStorage.read(TEAMS_DB)

        result = []

        for t in teams:
            result.append({
                "name": t["name"],
                "description": t["description"],
                "creation_time": t["creation_time"],
                "admin": t["admin"]
            })

        return json.dumps(result)

  
    # DESCRIBE TEAM
    def describe_team(self, request: str) -> str:

        data = json.loads(request)
        team_id = data["id"]

        teams = FileStorage.read(TEAMS_DB)

        for t in teams:
            if t["id"] == team_id:
                response = {
                    "name": t["name"],
                    "description": t["description"],
                    "creation_time": t["creation_time"],
                    "admin": t["admin"]
                }
                return json.dumps(response)

        raise Exception("Team not found")

    # UPDATE TEAM
    def update_team(self, request: str) -> str:

        data = json.loads(request)

        team_id = data["id"]
        team_data = data["team"]

        teams = FileStorage.read(TEAMS_DB)

        for t in teams:

            if t["id"] == team_id:

                if len(team_data["name"]) > 64:
                    raise Exception("Team name too long")

                if len(team_data["description"]) > 128:
                    raise Exception("Description too long")

                t["name"] = team_data["name"]
                t["description"] = team_data["description"]
                t["admin"] = team_data["admin"]

                FileStorage.write(TEAMS_DB, teams)

                return json.dumps({"status": "success"})

        raise Exception("Team not found")

    # ADD USERS TO TEAM
    def add_users_to_team(self, request: str):

        data = json.loads(request)

        team_id = data["id"]
        new_users = data["users"]

        teams = FileStorage.read(TEAMS_DB)

        for t in teams:

            if t["id"] == team_id:

                if len(t["users"]) + len(new_users) > 50:
                    raise Exception("Team cannot exceed 50 users")

                for u in new_users:
                    if u not in t["users"]:
                        t["users"].append(u)

                FileStorage.write(TEAMS_DB, teams)

                return json.dumps({"status": "success"})

        raise Exception("Team not found")

    # REMOVE USERS FROM TEAM
    def remove_users_from_team(self, request: str):

        data = json.loads(request)

        team_id = data["id"]
        users_to_remove = data["users"]

        teams = FileStorage.read(TEAMS_DB)

        for t in teams:

            if t["id"] == team_id:

                t["users"] = [u for u in t["users"] if u not in users_to_remove]

                FileStorage.write(TEAMS_DB, teams)

                return json.dumps({"status": "success"})

        raise Exception("Team not found")


    # LIST TEAM USERS
    def list_team_users(self, request: str):

        data = json.loads(request)

        team_id = data["id"]

        teams = FileStorage.read(TEAMS_DB)
        users = FileStorage.read(USERS_DB)

        for t in teams:

            if t["id"] == team_id:

                result = []

                for uid in t["users"]:

                    for u in users:

                        if u["id"] == uid:

                            result.append({
                                "id": u["id"],
                                "name": u["name"],
                                "display_name": u["display_name"]
                            })

                return json.dumps(result)

        raise Exception("Team not found")