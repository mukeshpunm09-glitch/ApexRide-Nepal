"""Rigid pricing logic for ApexRide Nepal — Rs. per day (NPR).
Server-side enforcement: any vehicle submission whose daily_price does
not match PRICE_MAP for its (category, tier) is rejected.
"""
PRICE_MAP = {
    ("cycle", "standard"): 500,
    ("cycle", "luxury"): 2000,
    ("bike", "standard"): 2000,
    ("bike", "luxury"): 7000,
    ("car", "standard"): 7000,
    ("car", "luxury"): 15000,
}

CATEGORY_LABELS = {"cycle": "Cycle", "bike": "Bike / Motorcycle", "car": "Car"}
TIER_LABELS = {"standard": "Standard", "luxury": "Luxury / High CC"}

SERVICE_FEE_RATE = 0.05   # 5%
VAT_RATE = 0.13            # 13% VAT (Nepal)
DEPOSIT_RATES = {"cycle": 5000, "bike": 15000, "car": 30000}


def get_daily_price(category, tier):
    """Return the locked daily price (Rs.) for a category/tier, or None."""
    return PRICE_MAP.get((str(category).lower(), str(tier).lower()))


def validate_price(category, tier, daily_price):
    """True only if daily_price exactly matches the rigid price map."""
    expected = get_daily_price(category, tier)
    return expected is not None and int(daily_price) == expected


def deposit_for(category, tier):
    base = DEPOSIT_RATES.get(str(category).lower(), 15000)
    return base * 2 if str(tier).lower() == "luxury" else base


def price_breakdown(daily_price, days, category="car", tier="standard"):
    """Automated booking breakdown. Returns dict of Rs. amounts (ints)."""
    days = max(1, int(days))
    daily_price = int(daily_price)
    subtotal = daily_price * days
    service_fee = round(subtotal * SERVICE_FEE_RATE)
    vat = round((subtotal + service_fee) * VAT_RATE)
    deposit = deposit_for(category, tier)
    total = subtotal + service_fee + vat
    return {
        "days": days, "daily_price": daily_price, "subtotal": subtotal,
        "service_fee": service_fee, "vat": vat, "deposit": deposit,
        "total": total, "payable_now": total + deposit,
    }
