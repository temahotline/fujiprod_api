from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.orders.models import OrderStatus
from src.orders.schemas import ShowOrder, OrderCreate, OrderUpdate
from src.orders.actions import (_update_order_by_id,
                                _create_new_order,
                                _get_orders,
                                _get_order_by_id)
from uuid import UUID


order_router = APIRouter()


@order_router.get("/{order_id}", response_model=ShowOrder)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)) -> Optional[ShowOrder]:
    order = await _get_order_by_id(order_id, db)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.post("/", response_model=ShowOrder)
async def create_order(
    order: OrderCreate, db: AsyncSession = Depends(get_db)
):
    created_order = await _create_new_order(order, db)
    return created_order


@order_router.patch("/{order_id}", response_model=ShowOrder)
async def update_order(
    order_id: UUID,
    body: OrderUpdate,
    db: AsyncSession = Depends(get_db),
):

    updated_order = await _update_order_by_id(
        order_id=order_id, body=body, db=db
    )
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@order_router.get("/", response_model=List[ShowOrder])
async def get_orders_list(
    user_id: Optional[UUID] = None,
    release_id: Optional[UUID] = None,
    status: Optional[OrderStatus] = None,
    page: int = 1,
    sort_by_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    orders = await _get_orders(
        user_id=user_id,
        release_id=release_id,
        status=status,
        page=page,
        sort_by_date=sort_by_date,
        db=db,
    )
    return orders
