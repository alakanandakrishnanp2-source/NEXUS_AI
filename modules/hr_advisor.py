
import re

from modules.vector_store import search_documents


STOP_WORDS = {
    "how", "many", "is", "are", "the", "for",
    "what", "a", "an", "of", "do", "does",
    "can", "i", "we", "our", "company",
    "employees", "employee", "allowed",
    "check", "all", "relevant", "documents",
    "identify", "conflicting", "information",
    "according", "uploaded", "policies",
    "clearly", "available", "entitlement",
    "days", "period"
}


def extract_annual_leave_days(text):
    """Extract annual leave entitlement values."""

    patterns = [
        r"\b(\d{1,3})\s*(?:calendar\s+)?days?\s+of\s+annual\s+leave\b",
        r"\bannual\s+leave(?:\s+entitlement)?\s*[:\-]?\s*(\d{1,3})\s*(?:calendar\s+)?days?\b",
        r"\bentitled\s+to\s+(\d{1,3})\s*(?:calendar\s+)?days?\s+of\s+annual\s+leave\b"
    ]

    values = set()

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:
            values.add(int(match))

    return values


def analyze_hr_question(question, user):

    if not question or not question.strip():
        raise ValueError("Please enter an HR question.")

    if not user:
        raise PermissionError("Please log in first.")

    user_role = user.get("role")

    if user_role not in ("admin", "standard"):
        raise PermissionError("Invalid user role.")

    question_lower = question.lower()

    # Detect the specific HR topics requested.
    topics = {
        "annual leave": [
            "annual leave",
            "annual leave entitlement"
        ],
        "maternity leave": [
            "maternity leave",
            "maternity"
        ],
        "paternity leave": [
            "paternity leave",
            "paternity"
        ],
        "probation period": [
            "probation period",
            "probation"
        ]
    }

    requested_topics = [
        topic
        for topic, keywords in topics.items()
        if any(keyword in question_lower for keyword in keywords)
    ]

    # A generic leave-entitlement question is treated as annual leave
    # only when maternity and paternity leave are not mentioned.
    if (
        not requested_topics
        and "leave entitlement" in question_lower
        and "maternity" not in question_lower
        and "paternity" not in question_lower
    ):
        requested_topics.append("annual leave")

    # Retrieve only authorized HR documents.
    documents = search_documents(
        question,
        top_k=10,
        user_role=user_role,
        category="hr"
    )

    if not documents:
        return {
            "answer": (
                "No relevant HR policy information was found "
                "in the authorized documents."
            ),
            "sources": []
        }

    sources = []
    evidence_by_topic = {
        topic: [] for topic in requested_topics
    }

    annual_leave_records = {}

    for document in documents:

        metadata = document.get("metadata", {})

        source = metadata.get(
            "source",
            "Unknown document"
        )

        page = metadata.get("page_number")

        content = document.get("text", "").strip()

        if not content:
            continue

        source_reference = (
            f"{source}, Page {page}"
            if page is not None
            else source
        )

        # Split document content into sentences.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            content
        )

        for sentence in sentences:

            sentence = sentence.strip()
            sentence_lower = sentence.lower()

            if not sentence:
                continue

            # Annual leave evidence.
            if "annual leave" in requested_topics:
                leave_values = extract_annual_leave_days(sentence)

                if leave_values:
                    annual_leave_records.setdefault(
                        source_reference,
                        set()
                    ).update(leave_values)

            # Collect evidence only for topics actually requested.
            for topic in requested_topics:

                topic_keywords = topics.get(topic, [])

                if any(
                    keyword in sentence_lower
                    for keyword in topic_keywords
                ):

                    item = (
                        f"{sentence} "
                        f"(Source: {source_reference})"
                    )

                    if item not in evidence_by_topic[topic]:
                        evidence_by_topic[topic].append(item)

    answer_parts = []

    # -------------------------------------------------
    # ANNUAL LEAVE CONFLICT DETECTION
    # -------------------------------------------------

    if "annual leave" in requested_topics:

        all_values = set()

        for values in annual_leave_records.values():
            all_values.update(values)

        if len(all_values) > 1:

            answer_parts.append(
                "### HR Policy Conflict Detected"
            )

            answer_parts.append(
                "The authorized HR documents contain "
                "different annual leave entitlements."
            )

            answer_parts.append(
                "**Annual Leave Comparison:**"
            )

            for source, values in annual_leave_records.items():
                for days in sorted(values):
                    answer_parts.append(
                        f"- {source}: {days} days of annual leave."
                    )

            answer_parts.append(
                "**Conflict:** The retrieved policies specify "
                f"different entitlements: "
                f"{', '.join(str(v) for v in sorted(all_values))} days."
            )

            answer_parts.append(
                "**Recommendation:** Refer this discrepancy "
                "to HR management for confirmation. Do not assume "
                "which policy is currently applicable."
            )

        elif len(all_values) == 1:

            days = next(iter(all_values))

            answer_parts.append(
                "### Annual Leave Information"
            )

            answer_parts.append(
                f"The retrieved HR documents specify "
                f"{days} days of annual leave."
            )

        else:

            answer_parts.append(
                "Annual leave entitlement is not clearly "
                "available in the retrieved HR documents."
            )

    # -------------------------------------------------
    # OTHER HR TOPICS
    # -------------------------------------------------

    for topic in requested_topics:

        if topic == "annual leave":
            continue

        answer_parts.append(
            f"### {topic.title()}"
        )

        topic_evidence = evidence_by_topic[topic]

        if topic_evidence:
            answer_parts.extend(
                f"- {item}" for item in topic_evidence
            )
        else:
            answer_parts.append(
                f"Information about {topic} is not available "
                "in the retrieved HR documents."
            )

    # -------------------------------------------------
    # GENERAL HR QUESTION
    # -------------------------------------------------

    if not requested_topics:

        answer_parts.append(
            "The HR Advisor could not identify a supported "
            "policy topic in the question. Please specify "
            "the HR policy you want to check."
        )

    # Collect only sources that contributed relevant evidence.
    for topic_evidence in evidence_by_topic.values():

        for item in topic_evidence:

            match = re.search(
                r"\(Source: (.+?)\)$",
                item
            )

            if match:
                source_reference = match.group(1)

                if source_reference not in sources:
                    sources.append(source_reference)

    # Include annual leave sources when annual leave was requested.
    if "annual leave" in requested_topics:

        for source in annual_leave_records:

            if source not in sources:
                sources.append(source)

    return {
        "answer": "\n\n".join(answer_parts),
        "sources": sources
    }
