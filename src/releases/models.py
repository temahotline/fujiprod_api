import uuid

from enum import Enum
from sqlalchemy import (Column, String, ForeignKey,
                        Integer, Date, Boolean, Text)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class ReleaseType(str, Enum):
    SINGLE = "SINGLE"
    EP = "EP"
    LP = "LP"
    MIXTAPE = "MIXTAPE"


class Release(Base):
    __tablename__ = "release"

    release_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False,
    )
    licensor_id = Column(
        UUID(as_uuid=True), ForeignKey("licensor.licensor_id"),
        nullable=False,
    )
    release_type = Column(
        SQLAlchemyEnum(ReleaseType, name="release_type"), nullable=False,
    )
    title = Column(String, nullable=False,)
    artist = Column(String, nullable=False,)
    release_date = Column(Date, nullable=True,)
    on_sale_date = Column(Date, nullable=False,)
    cover = Column(String, nullable=False,)
    genre = Column(String, nullable=False, )  # нужно будет создать модель жанра
    upc = Column(String, nullable=True, )

    tracks = relationship(
        "Track", back_populates="release", lazy="joined",
    )
    user = relationship(
        "User", back_populates="releases", lazy="joined",
    )
    licensor = relationship(
        "Licensor", back_populates="releases", lazy="joined",
    )


class Track(Base):
    __tablename__ = "track"

    track_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    release_id = Column(
        UUID(as_uuid=True),
        ForeignKey("release.release_id"),
        nullable=False,
    )
    title = Column(String, nullable=False,)
    artist = Column(String, nullable=False,)
    music_writer = Column(String, nullable=False,)
    text_writer = Column(String, nullable=False,)
    track = Column(String, nullable=False,)
    number_on_tracklist = Column(Integer, nullable=False,)
    tiktok_timing = Column(Integer, default=0,)
    explicit_content = Column(Boolean, nullable=False,)
    text = Column(Text, nullable=True)
    karaoke_text = Column(String, nullable=True)
    isrc = Column(String, nullable=True,)

    release = relationship(
        "Release", back_populates="tracks", lazy="joined",
    )
