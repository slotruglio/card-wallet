from fastapi import APIRouter

from ..model.wrapper import GiftCard

router = APIRouter(tags=["giftcard"])

@router.get("/")
async def read_giftcards() -> list[GiftCard]:
    return []