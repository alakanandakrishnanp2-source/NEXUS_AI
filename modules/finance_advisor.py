
import re

from modules.vector_store import search_documents
from modules.finance_calculator import calculate_financial_metrics


def extract_amount(text, keyword):
    """
    Extract an explicitly labelled financial amount.

    Examples:
        Revenue: AED 100000
        Total Expenses: AED 60000
    """

    patterns = {
        "revenue": (
            r"^\s*(?:total\s+)?revenue\s*[:\-]\s*"
            r"(?:AED\s*)?([\d,]+(?:\.\d+)?)\s*$"
        ),
        "expenses": (
            r"^\s*(?:(?:total|operating)\s+)?expenses\s*[:\-]\s*"
            r"(?:AED\s*)?([\d,]+(?:\.\d+)?)\s*$"
        )
    }

    if keyword not in patterns:
        raise ValueError("Unsupported financial metric.")

    match = re.search(
        patterns[keyword],
        text,
        re.IGNORECASE | re.MULTILINE
    )

    if match:
        return float(match.group(1).replace(",", ""))

    return None


def analyze_finances(question, user):

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    if not user:
        raise PermissionError("Please log in first.")

    user_role = user.get("role")

    if user_role not in ("admin", "standard"):
        raise PermissionError("Invalid user role.")

    normalized_question = question.lower()

    supported_terms = [
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

    # Do not calculate financial metrics for unrelated questions.
    if not any(
        term in normalized_question
        for term in supported_terms
    ):
        return {
            "answer": (
                "This question does not request a financial "
                "calculation currently supported by the Finance "
                "Advisor. Please check the authorized company "
                "documents using the General Advisor."
            ),
            "metrics": None,
            "sources": []
        }

    # Retrieve authorized financial documents.
    documents = search_documents(
        question,
        top_k=5,
        user_role=user_role,
        category="finance"
    )

    if not documents:
        return {
            "answer": (
                "No relevant financial information was found "
                "in the authorized financial documents."
            ),
            "metrics": None,
            "sources": []
        }

    financial_records = []

    for document in documents:

        text = document.get("text", "")
        metadata = document.get("metadata", {})

        revenue = extract_amount(text, "revenue")
        expenses = extract_amount(text, "expenses")

        if revenue is not None and expenses is not None:

            financial_records.append({
                "revenue": revenue,
                "expenses": expenses,
                "source": metadata.get(
                    "source",
                    "Unknown document"
                )
            })

    if not financial_records:
        return {
            "answer": (
                "The authorized financial documents do not contain "
                "clearly labelled revenue and expenses figures. "
                "A reliable calculation cannot be completed."
            ),
            "metrics": None,
            "sources": list(dict.fromkeys(
                document.get("metadata", {}).get(
                    "source", "Unknown document"
                )
                for document in documents
            ))
        }

    # Detect conflicting financial records.
    unique_pairs = {
        (record["revenue"], record["expenses"])
        for record in financial_records
    }

    sources = list(dict.fromkeys(
        record["source"]
        for record in financial_records
    ))

    if len(unique_pairs) > 1:
        return {
            "answer": (
                "Conflicting financial figures were found in "
                "the authorized financial documents. Please "
                "refer the discrepancy to Finance management "
                "for verification."
            ),
            "metrics": None,
            "sources": sources
        }

    # Calculate metrics using Python.
    record = financial_records[0]

    metrics = calculate_financial_metrics(
        revenue=record["revenue"],
        expenses=record["expenses"]
    )

    answer = (
        "### Financial Performance Analysis\n\n"
        f"**Revenue:** AED {metrics['revenue']:,.2f}\n\n"
        f"**Expenses:** AED {metrics['expenses']:,.2f}\n\n"
        f"**Net Profit:** AED {metrics['profit']:,.2f}\n\n"
        f"**Profit Margin:** {metrics['profit_margin']}%\n\n"
        f"The company generated a net profit of "
        f"AED {metrics['profit']:,.2f}, with a profit margin "
        f"of {metrics['profit_margin']}%.\n\n"
        f"**Sources:** {', '.join(sources)}\n\n"
        "Note: These figures are calculated from the "
        "retrieved authorized financial report."
    )

    return {
        "answer": answer,
        "metrics": metrics,
        "sources": sources
    }
