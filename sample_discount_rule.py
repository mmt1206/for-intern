DISCOUNT_TIERS = {
    "bronze": 0.05,
    "silver": 0.10,
    "gold": 0.15,
}


def calculate_discount(tier: str, amount: float) -> float:
    rate = DISCOUNT_TIERS.get(tier, 0.0)
    return round(amount * rate, 2)
