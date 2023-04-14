import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Date, ForeignKey

from src.database import Base


class Licensor(Base):
    __tablename__ = "licensor"

    licensor_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
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