import uuid

from enum import Enum
from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class ReleaseType(Enum):
    SINGLE = "single"
    EP = "ep"
    LP = "lp"
    MIXTAPE = "mixtape"


class Release(Base):
    __tablename__ = "releases"

    release_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False,
    )

    release_type = Column(
        SQLAlchemyEnum(ReleaseType, name="release_type"), nullable=False,
    )
    title = Column(String, nullable=False,)
    artist = Column(String, nullable=False,)
    release_date = Column(Date, nullable=True,)
    on_sale_date = Column(Date, nullable=False,)
    cover = Column(String, nullable=False,)
    tracks = relationship("Track", back_populates="release",)
    genre = Column(String, nullable=False,)  # нужно будет создать модель жанра
    upc = Column(String, nullable=True,)
    user = relationship("User", back_populates="releases",)


class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    release_id = Column(
        UUID(as_uuid=True),
        ForeignKey("releases.release_id"),
        nullable=False,
    )
    title = Column(String, nullable=False,)
    artist = Column(String, nullable=False,)
    track = Column(String, nullable=False,)
    number_on_tracklist = Column(Integer, nullable=False,)
    isrc = Column(String, nullable=True,)
    release = relationship("Release", back_populates="tracks")
