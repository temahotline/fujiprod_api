from typing import Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.orders.models import Order, OrderStatus


class OrderDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_order(self, user_id: UUID) -> UUID:
        new_order = Order(
            user_id=user_id,
            status=OrderStatus.CREATED
        )
        self.db_session.add(new_order)
        await self.db_session.flush()
        return new_order.order_id

    async def get_order_by_id(
            self, order_id: UUID) -> Union[Order, None]:
        pass

    async def update_order(
            self, order_id: UUID, **kwargs):
        pass


