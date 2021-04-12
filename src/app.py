import uvicorn
from fastapi import FastAPI
from .db import models, engine

models.Base.metadata.create_all(bind=engine)

DEBUG = True
DEV = 'DEV'
PROD = 'PROD'
PORT = 8000
ENV = DEV

app = FastAPI(debug=DEBUG,
              title='Linktious')

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
