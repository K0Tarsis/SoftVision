from fastapi import FastAPI, Query
from sqlalchemy import select, and_
from model import engine, users, games, connections

app = FastAPI()
conn = engine.connect()


@app.get("/get_games")
async def get_games(descriptions="Get all games, and users connected"):
    response = {}

    list_games = conn.execute(games.select())

    for id_game, name_game in list_games:
        command_users_in_game = select([users]).where(and_(connections.c.game_id == id_game,
                                                      connections.c.user_id == users.c.id))
        users_in_game = conn.execute(command_users_in_game)
        users_in_game = {user.id: user.name for user in users_in_game}
        response[id_game] = {"game_name": name_game, "users_in": users_in_game}

    return response


@app.get("/get_me/{user_id}")
async def get_me(user_id: int, descriptions="Get info about current user and info about all connected games"):
    command_user = users.select().where(users.c.id == user_id)
    user = conn.execute(command_user).fetchone()

    games_connected_command = select([games]).where(and_(connections.c.user_id == user.id,
                                                         connections.c.game_id == games.c.id))
    games_connected = conn.execute(games_connected_command)
    games_connected = {game.id: game.name for game in games_connected}

    return {"Id": user.id, "Name": user.name, "Age": user.age, "Email": user.email, "Connections": games_connected}


@app.post('/connect/{user_id}')
async def connect(user_id: int, game_id: int, descriptions="Create connection USER - GAME"):
    ins_connect = connections.insert().values(user_id=user_id, game_id=game_id)
    conn.execute(ins_connect)

    info = {"Game": game_id, "User": user_id}

    return {"Status": "Connected", "Info": info}


@app.post('/register')
async def register(name: str,
                   email: str = Query(regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"),
                   age: int = Query(ge=0, le=100),
                   descriptions="Register user"):
    ins_user = users.insert().values(name=name, age=age, email=email)
    conn.execute(ins_user)

    info = {"Name": name, "Age": age, "Email": email}

    return {"Status": "Registred", "Info": info}


@app.post('/create_game')
async def create_game(name: str, descriptions='Create game'):
    ins_game = games.insert().values(name=name)
    conn.execute(ins_game)

    info = {"Name": name}
    return {"Status": "Created", "Info": info}


@app.delete('/del_connection/{user_id}')
async def del_connect(user_id: int, game_id: int, descriptions='Delete USER-GAME connection'):
    del_connection = connections.delete().where(connections.c.user_id == user_id, connections.c.game_id == game_id)
    conn.execute(del_connection)

    info = {"Game": game_id, "User": user_id}

    return {"Status": "Deleted", "Info": info}
