import pytest

@pytest.mark.asyncio
def test_read_giftcards_empty(client):
    response = client.get("/giftcards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
def test_read_giftcards_with_data(client, sample_giftcard):
    response = client.get("/giftcards")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["supplier"] == "Amazon"

@pytest.mark.asyncio
def test_giftcards_filters(client, sample_giftcard):
    # filter by supplier
    response = client.get("/giftcards?supplier=Amazon")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    # filter by non-existing supplier
    response = client.get("/giftcards?supplier=Q8")
    data = response.json()
    assert len(data) == 0
