
import streamlit as st
from pathlib import Path
import uuid

from database.auth import authenticate_user
from database.audit_log import record_activity, get_audit_logs

from modules.advisor_router import route_question
from modules.document_processor import extract_text
from modules.text_chunker import create_chunks
from modules.vector_store import store_chunks, get_document_count


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# PROJECT DIRECTORIES
# ==========================================

DOCUMENT_FOLDER = Path("data/documents")
DOCUMENT_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================
# AUDIT LOGGING
# ==========================================

def log_activity(
    user,
    action,
    document_name=None,
    category=None,
    access_level=None,
    status="SUCCESS",
    details=None
):
    """Record application activity safely."""

    try:
        record_activity(
            username=user.get("username", "unknown"),
            action=action,
            document_name=document_name,
            category=category,
            access_level=access_level,
            status=status,
            details=details
        )

    except Exception as error:
        print("Audit logging error:", str(error))


# ==========================================
# SESSION STATE
# ==========================================

if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# APPLICATION HEADER
# ==========================================

def application_header():

    st.title("🤖 NEXUS AI")

    st.subheader(
        "Executive Advisory & Intelligence Platform"
    )

    st.divider()


# ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    application_header()

    st.markdown("### Welcome Back")

    st.write(
        "Please log in to access your NEXUS AI workspace."
    )

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        with st.form("login_form"):

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if submitted:

                if not username or not password:

                    st.error(
                        "Please enter both username and password."
                    )

                else:

                    try:

                        user = authenticate_user(
                            username,
                            password
                        )

                        if user:

                            st.session_state.user = user
                            st.session_state.chat_history = []

                            log_activity(
                                user=user,
                                action="USER_LOGIN",
                                status="SUCCESS",
                                details="User logged in successfully."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Invalid username or password."
                            )

                    except Exception as error:

                        st.error(
                            "Login failed. Please try again."
                        )

                        print("Login error:", str(error))


# ==========================================
# DOCUMENT MANAGEMENT
# ==========================================

def document_management(user):

    st.header("📁 Document Management")

    st.write(
        "Upload company documents to automatically "
        "extract, process, embed and index them."
    )

    if user.get("role") != "admin":

        st.error(
            "You are not authorized to upload documents."
        )

        return

    try:

        st.metric(
            "Indexed Document Chunks",
            get_document_count()
        )

    except Exception:

        st.warning(
            "Unable to retrieve document count."
        )

    st.divider()

    with st.form("document_upload_form"):

        uploaded_file = st.file_uploader(
            "Choose a document",
            type=["pdf", "docx", "txt"]
        )

        category = st.selectbox(
            "Document Category",
            ["general", "finance", "hr"]
        )

        access_level = st.selectbox(
            "Document Access Level",
            ["standard", "admin", "public"],
            help=(
                "Admin: administrators only. "
                "Standard: administrators and employees. "
                "Public: accessible to all authenticated users."
            )
        )

        upload_submitted = st.form_submit_button(
            "Upload and Index Document",
            use_container_width=True
        )

    if not upload_submitted:
        return

    if uploaded_file is None:

        st.error(
            "Please select a document first."
        )

        return

    file_path = None
    original_name = Path(uploaded_file.name).name

    try:

        # STEP 1: SAVE DOCUMENT

        unique_name = (
            f"{uuid.uuid4().hex[:8]}_{original_name}"
        )

        file_path = DOCUMENT_FOLDER / unique_name

        file_path.write_bytes(
            uploaded_file.getvalue()
        )

        st.info(
            f"Uploaded file: {original_name}"
        )

        # STEP 2: EXTRACT TEXT

        with st.spinner(
            "Extracting document text..."
        ):

            extracted_text = extract_text(
                str(file_path)
            )

        if not extracted_text or not extracted_text.strip():

            log_activity(
                user=user,
                action="DOCUMENT_UPLOAD_AND_INDEX",
                document_name=original_name,
                category=category,
                access_level=access_level,
                status="FAILED",
                details="No readable text found in document."
            )

            st.error(
                "No readable text was found in this document."
            )

            file_path.unlink(missing_ok=True)

            return

        # STEP 3: CREATE CHUNKS

        with st.spinner(
            "Creating document chunks..."
        ):

            chunks = create_chunks(
                extracted_text,
                source_file=str(file_path),
                chunk_size=500,
                chunk_overlap=50
            )

        if not chunks:

            log_activity(
                user=user,
                action="DOCUMENT_UPLOAD_AND_INDEX",
                document_name=original_name,
                category=category,
                access_level=access_level,
                status="FAILED",
                details="No document chunks were created."
            )

            st.error(
                "No document chunks were created."
            )

            file_path.unlink(missing_ok=True)

            return

        # STEP 4: APPLY ACCESS CONTROL METADATA

        for chunk in chunks:

            chunk["metadata"]["access_level"] = (
                access_level
            )

            chunk["metadata"]["category"] = (
                category
            )

            # Keep original filename for citations

            chunk["metadata"]["source"] = (
                original_name
            )

        # STEP 5: GENERATE EMBEDDINGS AND INDEX

        with st.spinner(
            "Generating embeddings and indexing document..."
        ):

            indexed_count = store_chunks(chunks)

        if indexed_count > 0:

            # STEP 6: RECORD SUCCESSFUL UPLOAD

            log_activity(
                user=user,
                action="DOCUMENT_UPLOAD_AND_INDEX",
                document_name=original_name,
                category=category,
                access_level=access_level,
                status="SUCCESS",
                details=(
                    f"{indexed_count} chunks indexed successfully."
                )
            )

            st.success(
                "Document uploaded and indexed successfully!"
            )

            st.write(
                f"**Document:** {original_name}"
            )

            st.write(
                f"**Category:** {category.title()}"
            )

            st.write(
                f"**Access Level:** {access_level.title()}"
            )

            st.write(
                f"**Chunks Indexed:** {indexed_count}"
            )

            st.info(
                "The document is now available "
                "for authorized AI searches."
            )

        else:

            log_activity(
                user=user,
                action="DOCUMENT_UPLOAD_AND_INDEX",
                document_name=original_name,
                category=category,
                access_level=access_level,
                status="FAILED",
                details="No document chunks were indexed."
            )

            st.warning(
                "No document chunks were indexed."
            )

    except Exception as error:

        log_activity(
            user=user,
            action="DOCUMENT_UPLOAD_AND_INDEX",
            document_name=original_name,
            category=category,
            access_level=access_level,
            status="FAILED",
            details=str(error)
        )

        st.error(
            "Document processing failed."
        )

        st.exception(error)


# ==========================================
# AUDIT LOG DASHBOARD
# ==========================================

def audit_log_dashboard():

    st.subheader("📋 System Audit Logs")

    st.write(
        "Monitor recent document uploads and system activities."
    )

    try:

        audit_logs = get_audit_logs(limit=50)

        if audit_logs:

            st.dataframe(
                audit_logs,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Showing {len(audit_logs)} recent activities."
            )

        else:

            st.info(
                "No audit activities recorded yet."
            )

    except Exception as error:

        st.error(
            "Unable to retrieve audit logs."
        )

        print("Audit display error:", str(error))


# ==========================================
# AI KNOWLEDGE ASSISTANT
# ==========================================

def ai_knowledge_assistant(user):

    st.header("💬 NEXUS AI Knowledge Assistant")

    st.write(
        "Ask questions about company documents, "
        "financial performance and HR policies."
    )

    # DISPLAY CHAT HISTORY

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):

            st.write(chat["question"])

        with st.chat_message("assistant"):

            st.markdown(
                f"**Selected Advisor:** {chat['advisor'].upper()}"
            )

            st.write(chat["answer"])

            if chat["sources"]:

                st.markdown("**Sources:**")

                for source in chat["sources"]:

                    st.write(f"- {source}")

            if chat["metrics"]:

                st.markdown("**Financial Metrics:**")

                st.json(chat["metrics"])

    # USER QUESTION

    question = st.chat_input(
        "Ask NEXUS AI a question..."
    )

    if question:

        with st.chat_message("user"):

            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "NEXUS AI is analysing your question..."
            ):

                try:

                    result = route_question(
                        question=question,
                        user=user
                    )

                    advisor = result.get(
                        "advisor",
                        "general"
                    )

                    answer = result.get(
                        "answer",
                        "No answer was generated."
                    )

                    sources = result.get("sources") or []

                    metrics = result.get("metrics")

                    st.markdown(
                        f"**Selected Advisor:** {advisor.upper()}"
                    )

                    st.write(answer)

                    if sources:

                        st.markdown("**Sources:**")

                        for source in sources:

                            st.write(f"- {source}")

                    if metrics:

                        st.markdown("**Financial Metrics:**")

                        st.json(metrics)

                    st.session_state.chat_history.append({

                        "question": question,
                        "advisor": advisor,
                        "answer": answer,
                        "sources": sources,
                        "metrics": metrics

                    })

                except Exception as error:

                    st.error(
                        "Unable to process your question."
                    )

                    st.exception(error)


# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin_dashboard(user):

    st.title("Administrator Dashboard")

    st.success(
        f"Welcome, {user.get('username', 'Administrator')}!"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("AI Advisors", "3")

    with col2:

        st.metric(
            "Knowledge Base",
            get_document_count()
        )

    with col3:

        st.metric(
            "Access Level",
            "Administrator"
        )

    st.divider()

    # ADMIN DOCUMENT MANAGEMENT

    document_management(user)

    st.divider()

    # AUDIT LOGS

    audit_log_dashboard()

    st.divider()

    st.subheader("Available Features")

    st.markdown(
        """
        - Document Management
        - AI Knowledge Assistant
        - Finance Advisor
        - HR & Management Advisor
        - General Business Intelligence
        - User Access Management
        - System Audit Logging
        """
    )

    st.divider()

    ai_knowledge_assistant(user)


# ==========================================
# STANDARD USER DASHBOARD
# ==========================================

def standard_dashboard(user):

    st.title("Employee Dashboard")

    st.success(
        f"Welcome, {user.get('username', 'Employee')}!"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("AI Advisors", "3")

    with col2:

        st.metric(
            "Knowledge Base",
            get_document_count()
        )

    with col3:

        st.metric(
            "Access Level",
            "Standard User"
        )

    st.info(
        "Your access is restricted to documents "
        "and information authorized for Standard Users."
    )

    st.divider()

    ai_knowledge_assistant(user)


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    if st.session_state.user is None:

        login_page()

    else:

        user = st.session_state.user

        with st.sidebar:

            st.title("🤖 NEXUS AI")

            st.write(
                f"User: {user.get('username', 'User')}"
            )

            st.write(
                f"Role: {user.get('role', 'Unknown').title()}"
            )

            st.divider()

            if st.button(
                "Logout",
                use_container_width=True
            ):

                log_activity(
                    user=user,
                    action="USER_LOGOUT",
                    status="SUCCESS",
                    details="User logged out."
                )

                st.session_state.user = None
                st.session_state.chat_history = []

                st.rerun()

        role = user.get("role")

        if role == "admin":

            admin_dashboard(user)

        elif role == "standard":

            standard_dashboard(user)

        else:

            st.error("Invalid user role.")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    main()
