from decimal import Decimal

TAXES: Decimal = Decimal("0.08")
CURRENCY: str = "$"


def calculate_subtotal(items: dict[str, dict[str, str]]) -> str:
    all_prices: list[str] = list()
    for internal_dict in items.values():
        all_prices.append(internal_dict["price"])

    all_prices_with_no_currency_sign: list[Decimal] = [
        Decimal(price[1:]) for price in all_prices
    ]
    total: Decimal = sum(all_prices_with_no_currency_sign, Decimal("0"))
    return f"{CURRENCY}{total:.2f}"


def calculate_taxes(items: dict[str, dict[str, str]]) -> str:
    subtotal: str = calculate_subtotal(items)
    total_without_currency = Decimal(subtotal[1:])

    taxes: Decimal = round(total_without_currency * TAXES, 2)
    return f"{CURRENCY}{taxes:.2f}"


def calculate_total(items: dict[str, dict[str, str]]) -> str:
    subtotal = Decimal(calculate_subtotal(items)[1::])
    taxes = Decimal(calculate_taxes(items)[1::])

    total: Decimal = subtotal + taxes
    return f"{CURRENCY}{total:.2f}"
