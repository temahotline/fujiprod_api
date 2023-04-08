import uuid

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class Release(Base):
    __tablename__ = "releases"

    release_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(),
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False,
    )
    release_type = Column()
    title = Column(String, nullable=False,)
    artist = Column(String, nullable=False,)
    cover = Column()
    tracks = Column()
    genre = Column()
    upc = Column(String, nullable=True,)
    user = relationship("User", back_populates="releases", )


class Track(Base):
    __tablename__ = "tracks"

    release_id = Column(
        UUID(as_uuid=True),
        ForeignKey("releases.release_id"),
        nullable=False,
    )
    title = Column(String, nullable=False,)
    artist = Column(String, nullable=False,)
    track = Column()
    number = Column(Integer, nullable=False,)
