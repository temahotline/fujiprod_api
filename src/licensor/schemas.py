import uuid
from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.users.schemas import ShowUser


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


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


class UpdatedLicensorResponse(BaseModel):
    full_name: Optional[str] = None
    birthday: Optional[date] = None
    passport_number: Optional[str] = None
    passport_issue_date: Optional[date] = None
    registration: Optional[str] = None