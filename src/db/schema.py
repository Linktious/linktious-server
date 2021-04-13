from typing import Optional, List, Union
import datetime as dt
from pydantic import BaseModel


class IdOnly(BaseModel):
    id: int

    class Config:
        orm_mode = True 


class TeamBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int


class UserBase(BaseModel):
    name: str
    email: str
    is_active: bool = True
    team_id: int = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    hashed_password: str


class UserBasicInfo(UserBase):
    id: int


class User(UserBasicInfo):
    main_board_id: int = None
    favorite_boards: List[IdOnly] = []


class LabelBase(BaseModel):
    name: str
    created_at: dt.datetime
    created_by_user_id: int

    class Config:
        orm_mode = True


class LabelCreate(LabelBase):
    pass


class Label(LabelBase):
    id: int


class LinkBase(BaseModel):
    icon_url: str
    url: str
    created_at: dt.datetime
    created_by_user_id: int
    labels: List[IdOnly] = []

    class Config:
        orm_mode = True


class LinkCreate(LinkBase):
    pass


class Link(LinkBase):
    id: int


class BoardBase(BaseModel):
    name: str
    description: str
    created_at: dt.datetime
    updated_at: dt.datetime
    created_by_user_id: int
    labels_filters: List[IdOnly] = []

    class Config:
        orm_mode = True


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: int
