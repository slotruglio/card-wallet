import pytest

@pytest.mark.asyncio
async def test_read_users_empty(client):
    response = await client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_users_with_data(client, sample_user):
    response = await client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "John Doe"
