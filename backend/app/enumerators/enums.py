from enum import Enum

class GiftCardSpentFilter(str, Enum):
    unused = "unused"
    partial = "partial"
    full = "full"

class GiftCardSortField(str, Enum):
    created_at = "created_at"
    supplier = "supplier"
    amount = "amount"
    spent_amount = "spent_amount"

class SortOrderFilter(str, Enum):
    desc = "desc"
    asc = "asc"
    
