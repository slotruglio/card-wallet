from .gift_card import GiftCard
from .user import User

# After both classes exist
User.model_rebuild()
GiftCard.model_rebuild()
