import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

meta = MetaData()

users = Table("Users", meta,
              Column("id", Integer, primary_key=True),
              Column("name", String(30), nullable=False),
              Column('age', Integer, nullable=False),
              Column('email', String(60), nullable=False)
              )

games = Table("Games", meta,
              Column("id", Integer, primary_key=True),
              Column("name", String(30), nullable=False)
              )

connections = Table("Connections", meta,
                    Column("id", Integer, primary_key=True),
                    Column("user_id", Integer, ForeignKey("Users.id")),
                    Column("game_id", Integer, ForeignKey("Games.id"))
                    )

if os.environ.get("DATABASE_POSTGRES"):
    DATABASE = os.environ.get("DATABASE_POSTGRES")
else:
    DATABASE = "localhost"

engine = create_engine(f"postgresql+psycopg2://root:root@{DATABASE}/softvision")


if __name__ == "__main__":
    meta.create_all(engine)
    conn = engine.connect()

    ins_user1 = users.insert().values(name="Kostia", age=23, email="kostia@gmail.com")
    conn.execute(ins_user1)
    ins_user2 = users.insert().values(name="Andriy", age=22, email="andriy@gmail.com")
    conn.execute(ins_user2)
    ins_user3 = users.insert().values(name="Vova", age=21, email="vova@gmail.com")
    conn.execute(ins_user3)

    ins_game1 = games.insert().values(name="Smite")
    conn.execute(ins_game1)
    ins_game2 = games.insert().values(name="Survarium")
    conn.execute(ins_game2)

    ins_connect = connections.insert().values(user_id=1, game_id=1)
    conn.execute(ins_connect)
