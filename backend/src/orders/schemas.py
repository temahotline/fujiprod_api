from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.orders.models import OrderStatus
from src.releases.schemas import ShowRelease


class OrderCreate(BaseModel):
    user_id: UUID


class OrderUpdate(BaseModel):
    user_id: UUID
    status: OrderStatus
    release_id: Optional[UUID] = None


class ShowOrder(BaseModel):
    order_id: UUID
    user_id: UUID
    release: Optional[ShowRelease]
    status: OrderStatus
    created: datetime

    class Config:
        orm_mode = True
