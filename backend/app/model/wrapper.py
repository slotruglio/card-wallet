from .gift_card import GiftCard, GiftCardORM
from .user import User, UserORM

# After both classes exist
User.model_rebuild()
GiftCard.model_rebuild()
