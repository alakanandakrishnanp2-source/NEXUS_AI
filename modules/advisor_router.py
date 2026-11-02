
from modules.finance_advisor import analyze_finances
from modules.hr_advisor import analyze_hr_question
from modules.rag_engine import ask_nexus


# Only include financial topics that the Finance Advisor
# can currently calculate or analyze reliably.
FINANCE_KEYWORDS = [
    "revenue",
    "expenses",
    "expense",
    "net profit",
    "profit margin",
    "profitability",
    "financial performance",
    "financial report",
    "finance report",
    "cash flow",
    "operating expenses"
]

HR_KEYWORDS = [
    "annual leave",
    "sick leave",
    "maternity leave",
    "working hours",
    "attendance",
    "remote work",
    "hr policy",
    "human resources",
    "manager approval",
    "leave policy",
    "recruitment",
    "staff policy",
    "employee benefits",
    "employee policy",
    "employee leave",
    "employee attendance"
]


def classify_question(question):

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    normalized = question.lower()

    finance_matches = [
        keyword for keyword in FINANCE_KEYWORDS
        if keyword in normalized
    ]

    hr_matches = [
        keyword for keyword in HR_KEYWORDS
        if keyword in normalized
    ]

    # Mixed Finance and HR questions go to General
    # because neither specialist currently handles both.
    if finance_matches and hr_matches:
        return "general"

    if finance_matches:
        return "finance"

    if hr_matches:
        return "hr"

    # Unsupported financial requests, such as marketing
    # budgets, should be checked against company documents.
    return "general"


def route_question(question, user):

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    if not user:
        raise PermissionError("Please log in first.")

    if user.get("role") not in ("admin", "standard"):
        raise PermissionError("Invalid user role.")

    advisor = classify_question(question)

    print(f"Selected Advisor: {advisor.upper()}")

    if advisor == "finance":
        result = analyze_finances(question, user)

    elif advisor == "hr":
        result = analyze_hr_question(question, user)

    else:
        result = ask_nexus(question, user)

    return {
        "advisor": advisor,
        "answer": result.get(
            "answer",
            "No answer could be generated."
        ),
        "sources": result.get("sources", []),
        "metrics": result.get("metrics")
    }
