from typing import List, Optional
from uuid import UUID
from src.orders.dals import OrderDAL
from src.orders.schemas import OrderCreate, OrderUpdate, OrderInDB
from src.orders.models import OrderStatus
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_new_order(body: OrderCreate, db: AsyncSession) -> OrderInDB:
    async with db as session:
        async with session.begin():
            order_dal = OrderDAL(session)
            order = await order_dal.create_order(user_id=body.user_id)
            return order


async def _update_order_by_id(order_id: UUID, body: OrderUpdate, db: AsyncSession) -> OrderInDB:
    async with db as session:
        async with session.begin():
            order_dal = OrderDAL(session)
            order = await order_dal.update_order(order_id, **body.dict())
            if order is not None:
                return order


async def _get_orders(
    user_id: Optional[UUID],
    release_id: Optional[UUID],
    status: Optional[OrderStatus],
    page: int,
    sort_by_date: Optional[str],
    db: AsyncSession,
) -> List[OrderInDB]:
    async with db as session:
        async with session.begin():
            order_dal = OrderDAL(session)
            orders = await order_dal.get_orders(
                user_id=user_id,
                release_id=release_id,
                status=status,
                page=page,
                sort_by_date=sort_by_date,
            )
            return orders


async def _get_order_by_id(order_id: UUID, db) -> Optional[OrderInDB]:
    async with db as session:
        async with session.begin():
            order_dal = OrderDAL(session)
            order = await order_dal.get_order_by_id(order_id)
            if order is not None:
                return order
