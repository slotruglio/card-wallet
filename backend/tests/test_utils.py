import asyncio
import pytest


def test_assertion():
    assert 1 + 1 == 2
    
@pytest.mark.asyncio
async def test_asyncio():
    await asyncio.sleep(0.5)