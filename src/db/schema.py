from typing import List
from datetime import datetime
from pydantic import BaseModel, validator, HttpUrl, EmailStr


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
    email: EmailStr
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
    favorite_boards: List[int] = []

    @validator("favorite_boards", pre=True)
    def favorite_boards_ids(cls, favorite_boards):
        return (board.id for board in favorite_boards)

    class Config:
        orm_mode = True


class LabelBase(BaseModel):
    name: str
    created_at: datetime
    created_by_user_id: int


class LabelCreate(LabelBase):
    
    class Config:
        orm_mode = True


class Label(LabelBase):
    id: int

    class Config:
        orm_mode = True


class LinkBase(BaseModel):
    icon_url: HttpUrl
    url: HttpUrl
    created_at: datetime
    created_by_user_id: int


class LinkCreate(LinkBase):
    
    class Config:
        orm_mode = True


class Link(LinkBase):
    id: int
    labels: List[int] = []

    @validator("labels", pre=True)
    def labels_ids(cls, labels):
        return (label.id for label in labels)

    class Config:
        orm_mode = True


class BoardBase(BaseModel):
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    created_by_user_id: int


class BoardCreate(BoardBase):
    
    class Config:
        orm_mode = True


class Board(BoardBase):
    id: int
    labels_filters: List[int] = []

    @classmethod
    @validator("labels_filters", pre=True)
    def labels_ids(cls, labels):
        return (label.id for label in labels)

    class Config:
        orm_mode = True
