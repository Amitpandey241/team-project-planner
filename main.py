from services.user_service import UserService
from services.team_service import TeamService
from services.board_service import BoardService


service = UserService()
team_service = TeamService()
board_service = BoardService()

# USER CREATION, LIST USER, DESCRIBE USER, UPDATE USER, GET USER BY TEAM

# print(service.create_user(
# '{"name":"Abhi","display_name":"Abhi Pandey"}'
# ))

# print(service.list_users())

# print(service.describe_user('{"id":"1"}'))

# print(service.update_user(
# '{"id":"1","user":{"name":"amit","display_name":"Amit Pandey"}}'
# ))

# print(service.get_user_teams('{"id":"1"}'))


# TEAMS: CREATE, LIST TEAMS, DESCRIBE TEAM, ADD USER IN TEAM, LIST TEAM USERS

# print(team_service.create_team(
# '{"name":"Backend Team","description":"API Development","admin":"1"}'
# ))

# print(team_service.list_teams())

# print(team_service.describe_team('{"id":"1"}'))

# print(team_service.add_users_to_team(
# '{"id":"1","users":["2"]}'
# ))

# print(team_service.list_team_users('{"id":"1"}'))

# BORAD: CREATE, LIST BOARD, ADD TASK, UPDATE TASK AND EXPORT BOARD 

# print(board_service.create_board(
# '{"name":"Sprint 1","description":"Login feature","team_id":"1","creation_time":"2026-03-10"}'
# ))

# print(board_service.list_boards('{"id":"1"}'))

# print(board_service.add_task(
# '{"board_id":"1","title":"Login API","description":"Implement JWT","user_id":"1","creation_time":"2026-03-10"}'
# ))


# print(board_service.update_task_status(
# '{"id":"1","status":"COMPLETE"}'
# ))

# print(board_service.export_board('{"id":"1"}'))