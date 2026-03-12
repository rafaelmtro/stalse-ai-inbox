import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_ticket():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tickets", json={
            "customer_name": "John Doe",
            "message": "My internet is not working"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert "id" in data
    assert "category" in data
    assert "priority" in data

@pytest.mark.asyncio
async def test_get_tickets():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_ticket():
    # First create a ticket
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_res = await ac.post("/tickets", json={
            "customer_name": "Jane Doe",
            "message": "Billing issue"
        })
        ticket_id = create_res.json()["id"]
        
        # Then update it
        update_res = await ac.patch(f"/tickets/{ticket_id}", json={
            "status": "resolved",
            "priority": "low"
        })
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "resolved"
