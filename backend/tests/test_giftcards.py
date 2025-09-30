from httpx import Response
import pytest

@pytest.mark.asyncio
async def test_read_giftcards_empty(client):
    response: Response = await client.get("/giftcards")
    assert response.status_code == 200
    data = response.json()
    print("here", data)
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_read_giftcards_with_data(client, sample_giftcard):
    response = await client.get("/giftcards")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["supplier"] == "Amazon"

@pytest.mark.asyncio
async def test_giftcards_filters(client, sample_giftcard):
    # filter by supplier
    response = await client.get("/giftcards?supplier=Amazon")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    # filter by non-existing supplier
    response = await client.get("/giftcards?supplier=Q8")
    data = response.json()
    assert len(data) == 0
