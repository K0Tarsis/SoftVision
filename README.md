# SoftVision
Was used FastAPI and Uvicorn, SQLAlchemy, PostgreSQL

To install requirments comand "pip install -r requirements.txt" in your virtual environment. 

To run project "uvicorn main:app --reload"

To initialize the database, need first run model.py "python model.py"

Available endpoints:
  1) GET(/get_games) #Get all games, and users connected
  2) GET(/get_me/{user_id}) #Get info about current user and info about all connected games
  3) POST(/connect/{user_id}?game_id=_) #Create connection USER - GAME
  4) POST(/register?name=_&email=_&age=_) #Register user
  5) POST(/create_game?name=_) #Create game
  6) DELETE(/del_connection/{user_id}?game_id=_) # Delete USER-GAME connection
