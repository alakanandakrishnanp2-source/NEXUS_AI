
from decimal import Decimal, InvalidOperation


def calculate_financial_metrics(revenue, expenses):
    """
    Calculate profit and profit margin using Python.
    """

    try:
        revenue = Decimal(str(revenue))
        expenses = Decimal(str(expenses))

    except (InvalidOperation, ValueError):
        raise ValueError("Revenue and expenses must be valid numbers.")

    if not revenue.is_finite() or not expenses.is_finite():
        raise ValueError("Financial values must be finite numbers.")

    if revenue < 0 or expenses < 0:
        raise ValueError("Revenue and expenses cannot be negative.")

    if revenue == 0:
        raise ValueError("Revenue must be greater than zero.")

    # Calculate net profit
    profit = revenue - expenses

    # Calculate profit margin
    profit_margin = (profit / revenue) * Decimal("100")

    return {
        "revenue": float(revenue),
        "expenses": float(expenses),
        "profit": float(profit),
        "profit_margin": round(float(profit_margin), 2)
    }

