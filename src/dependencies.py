from sqlalchemy.orm import Session
from db import base


def get_db() -> Session:
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()
