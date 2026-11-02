
from modules.finance_calculator import calculate_financial_metrics


revenue = 100000
expenses = 60000

print("NEXUS AI - FINANCE CALCULATOR")
print("=" * 40)

try:
    result = calculate_financial_metrics(
        revenue,
        expenses
    )

    print("Revenue:", result["revenue"])
    print("Expenses:", result["expenses"])
    print("Net Profit:", result["profit"])
    print("Profit Margin:", result["profit_margin"], "%")

except ValueError as error:
    print("Calculation Error:", error)
