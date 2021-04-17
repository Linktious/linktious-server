import uvicorn
from fastapi import FastAPI, status
from sqlalchemy.orm import Session

from db import base
from routers import (
    users,
    teams,
    labels,
    links,
    boards,
) 

base.Base.metadata.create_all(bind=base.engine)

DEBUG = True
DEV = 'DEV'
PROD = 'PROD'
PORT = 8000
ENV = DEV


app = FastAPI(
    debug=DEBUG,
    title='Linktious',
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"}
    }
)


app.include_router(users.router)
app.include_router(teams.router)
app.include_router(labels.router)
app.include_router(links.router)
app.include_router(boards.router)


# TODO: routes that has created_by should get the user id from request and not as param.
@app.get("/")
def read_root():
    return {"status": "OK"}


@app.get("/health")
def health_check():
    return {"status": "Ok"}


def start():
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level="info", reload=ENV == DEV)


if __name__ == "__main__":
    start()
