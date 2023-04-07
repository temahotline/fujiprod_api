import uuid

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    sign_up_source: str
    id_on_source: str


class UserCreate(BaseModel):
    sign_up_source: str
    id_on_source: str
