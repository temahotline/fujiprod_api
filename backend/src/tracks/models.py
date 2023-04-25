import uuid

from sqlalchemy import (Column, String, ForeignKey,
                        Integer, Boolean, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class Track(Base):
    __tablename__ = "track"

    track_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
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
    text = Column(Text, nullable=True,)
    karaoke_text = Column(String, nullable=True,)
    isrc = Column(String, nullable=True,)

    release = relationship(
        "Release", back_populates="tracks", lazy="joined",
    )
