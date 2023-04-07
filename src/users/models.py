import uuid

from enum import Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String


Base = declarative_base()


class SignUpSource(Enum):
    VK = "vk"
    TELEGRAM = "telegram"
    WEBSITE = "website"


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    sign_up_source = Column(Enum(SignUpSource), nullable=False,)
    id_on_source = Column(String, nullable=False,)

