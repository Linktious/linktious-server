from typing import Optional, List, Union
import datetime as dt
from pydantic import BaseModel


class IdOnly(BaseModel):
    id: int

    class Config:
        orm_mode = True 


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    
    class Config:
        orm_mode = True


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    is_active: bool = True
    team_id: int = None


class UserCreate(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserBasicInfo(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBasicInfo):
    main_board_id: int = None
    favorite_boards: List[IdOnly] = []

    class Config:
        orm_mode = True


class LabelBase(BaseModel):
    name: str
    created_at: dt.datetime
    created_by_user_id: int


class LabelCreate(LabelBase):
    
    class Config:
        orm_mode = True


class Label(LabelBase):
    id: int

    class Config:
        orm_mode = True


class LinkBase(BaseModel):
    icon_url: str
    url: str
    created_at: dt.datetime
    created_by_user_id: int


class LinkCreate(LinkBase):
    
    class Config:
        orm_mode = True


class Link(LinkBase):
    id: int
    labels: List[IdOnly] = []

    class Config:
        orm_mode = True


class BoardBase(BaseModel):
    name: str
    description: str
    created_at: dt.datetime
    updated_at: dt.datetime
    created_by_user_id: int


class BoardCreate(BoardBase):
    
    class Config:
        orm_mode = True


class Board(BoardBase):
    id: int
    labels_filters: List[IdOnly] = []

    class Config:
        orm_mode = True
