from .gift_card import GiftCard
from .user import User
from .file import FileRead

# After both classes exist
User.model_rebuild()
GiftCard.model_rebuild()
FileRead.model_rebuild()
