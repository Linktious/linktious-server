from db.base import *
from db import models, schema

models.Base.metadata.create_all(bind=engine)
ses = SessionLocal()


def generate_db():
    Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    def add(*objs):
        ses.add_all(objs)
        ses.commit()
        for obj in objs:
            ses.refresh(obj)
        return objs

    team1 = models.Team(name="Team Rocket")
    add(team1)

    user1 = models.User(name="Asaf", email="user@email.com", hashed_password="12345678", team_id=team1.id)
    add(user1)

    link1 = models.Link(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/768px-Python.svg.png", url="https://docs.python.org/3/", description="Python Documentation", created_by_user_id=user1.id)
    link2 = models.Link(icon_url="https://cdn.worldvectorlogo.com/logos/redis.svg", url="https://redis.io/documentation", description="Redis Documentation", created_by_user_id=user1.id)
    link3 = models.Link(icon_url="http://www.icon3.com", url="http://url1.com", description="link3", created_by_user_id=user1.id)
    add(link1, link2, link3)

    label1 = models.Label(name="Python", created_by_user_id=user1.id)
    label2 = models.Label(name="Documentations", created_by_user_id=user1.id)
    label3 = models.Label(name="Redis", created_by_user_id=user1.id)
    add(label1, label2, label3)

    link1.labels.append(label1)
    link1.labels.append(label2)
    link2.labels.append(label2)
    link2.labels.append(label3)
    link3.labels.append(label1)
    link3.labels.append(label3)
    ses.commit()

    board1 = models.Board(name="board1", description="my cool board", created_by_user_id=user1.id)
    add(board1)

    user1.favorite_boards.append(board1)
    user1.main_board_id = board1.id

    board1.labels_filters.append(label2)
    ses.commit()


generate_db()

teams = ses.query(models.Team).all()
users = ses.query(models.User).all()
links = ses.query(models.Link).all()
labels = ses.query(models.Label).all()
boards = ses.query(models.Board).all()


# ipython -i playground.py