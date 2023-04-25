from typing import Union, Optional, List
from uuid import UUID

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.orders.models import Order, OrderStatus


PAGE_SIZE: int = 10


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
        query = select(Order).where(Order.order_id == order_id)
        res = await self.db_session.execute(query)
        order_row = res.fetchone()
        if order_row is not None:
            return order_row[0]

    async def update_order(
            self, order_id: UUID, **kwargs) -> Union[Order, None]:
        query = (
            update(Order)
            .where(Order.order_id == order_id)
            .values(kwargs)
            .returning(Order)
        )
        res = await self.db_session.execute(query)
        update_order_row = res.fetchone()
        if update_order_row is not None:
            return update_order_row[0]

    async def get_orders(
            self,
            user_id: Optional[UUID] = None,
            release_id: Optional[UUID] = None,
            status: Optional[OrderStatus] = None,
            sort_by_date: Optional[str] = None,
            page: int = 1
    ) -> List[Order]:
        query = select(Order)

        conditions = []
        if user_id is not None:
            conditions.append(Order.user_id == user_id)
        if release_id is not None:
            conditions.append(Order.release_id == release_id)
        if status is not None:
            conditions.append(Order.status == status)

        if conditions:
            query = query.where(and_(*conditions))

        if sort_by_date:
            if sort_by_date.lower() == "asc":
                query = query.order_by(Order.created.asc())
            elif sort_by_date.lower() == "desc":
                query = query.order_by(Order.created.desc())

        offset = (page - 1) * PAGE_SIZE
        query = query.limit(PAGE_SIZE).offset(offset)

        res = await self.db_session.execute(query)
        orders = res.fetchall()
        return [order for order, in orders]
