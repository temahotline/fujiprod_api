import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    UNDER_REVIEW = "UNDER_REVIEW"
    PROBLEM = "PROBLEM"
    COMPLETED = "COMPLETED"


class Order(Base):
    __tablename__ = "order"

    order_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    release_id = Column(
        UUID(as_uuid=True),
        ForeignKey("release.release_id"),
        nullable=False,
    )
    status = Column(SQLAlchemyEnum(OrderStatus, name="order_status"),
                    default=OrderStatus.CREATED, nullable=False,)
    created = Column(DateTime, default=datetime.utcnow,)

    user = relationship("User", back_populates="orders",)
    c = relationship("Release", back_populates="order",)
