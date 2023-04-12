import uuid
from datetime import date

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


class ShowLicensor(TunedModel):
    licensor_id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    birthday: date
    passport_number: str
    passport_issue_date: date
    registration: str
    user: ShowUser


class LicensorCreate(BaseModel):
    user_id: uuid.UUID
    full_name: str
    birthday: date
    passport_number: str
    passport_issue_date: date
    registration: str
