import uuid

from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from src.database import Base


class SignUpSource(str, Enum):
    VK = "VK"
    TELEGRAM = "TELEGRAM"
    WEBSITE = "WEBSITE"


class User(Base):
    __tablename__ = "user"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    sign_up_source = Column(SQLAlchemyEnum(
        SignUpSource, name="sign_up_source"), nullable=False,
    )
    id_on_source = Column(String, nullable=False,)

    licensors = relationship("Licensor", back_populates="user",)
    releases = relationship("Release", back_populates="user",)


class Licensor(Base):
    __tablename__ = "licensor"

    licensor_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False,
    )
    full_name = Column(String, nullable=False,)
    birthday = Column(Date, nullable=False,)
    passport_number = Column(String, nullable=False,)
    passport_issue_date = Column(Date, nullable=False,)
    registration = Column(String, nullable=False,)

    user = relationship(
        "User", back_populates="licensors",
    )
    releases = relationship(
        "Release", back_populates="licensor",
    )
