import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from main import app
from database.models import init_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    await init_db()
    yield

@pytest.mark.asyncio
async def test_create_ticket():
    # Mock AI Service to avoid real API calls in tests
    mock_ai_result = {"category": "Technical Support", "priority": "high"}
    
    with patch("services.ai.gemini.ai_service.classify_ticket", new_callable=AsyncMock) as mock_classify:
        mock_classify.return_value = mock_ai_result
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/tickets", json={
                "customer_name": "John Doe",
                "message": "My internet is not working"
            })
            
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["category"] == "Technical Support"
    assert data["priority"] == "high"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_tickets():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_ticket():
    # Mock AI for creation part
    mock_ai_result = {"category": "Billing", "priority": "low"}
    
    with patch("services.ai.gemini.ai_service.classify_ticket", new_callable=AsyncMock) as mock_classify:
        mock_classify.return_value = mock_ai_result
        
        transport = ASGITransport(app=app)
        # First create a ticket
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
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
