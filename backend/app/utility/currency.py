from decimal import Decimal

def currency_to_int(a: Decimal) -> int:
    return round(a * 100) 

def int_to_currency(a: int) -> Decimal:
    return a / 100