from src.orders.models import OrderStatus, Order
from tests.conftest import client, async_session_maker


async def test_update_order_with_invalid_status(order):
    order_id = str(order.order_id)
    order_data = {
        "status": "invalid",
    }
    response = client.patch(f"/orders/{order_id}", json=order_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


async def test_create_order_and_check_status(user):
    user_id = str(user.user_id)
    order_data = {
        "user_id": user_id,
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    async with async_session_maker() as session:
        async with session.begin():
            order = await session.get(Order, response.json()["order_id"])
            assert order.status == OrderStatus.CREATED
