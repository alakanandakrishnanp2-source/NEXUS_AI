
# NEXUS AI – Executive Advisory & Intelligence Platform

NEXUS AI is a proof-of-concept, AI-powered knowledge and advisory application designed to help authorized users interact with company documents through specialized AI advisors.

The platform supports General, Finance, and HR advisory routes, document processing, role-based access control, retrieval-augmented generation (RAG), and audit logging.

> **Project Status:** Demonstration proof-of-concept. This is not a production-ready enterprise system.

## 1. Implemented Capabilities

- **Authentication:** Login through the application's existing SQLite authentication module.
- **Role-Based Access Control:** Supports Admin and Standard user roles.
- **Document Management:** Admin users can upload PDF, DOCX, and TXT files.
- **Document Processing:** Text extraction, chunking, metadata assignment, embedding generation, and indexing.
- **Retrieval-Augmented Generation (RAG):** General Advisor retrieves authorized General-category document chunks and uses Gemini to generate answers.
- **Specialized Advisors:** Finance and HR questions are routed to their respective advisor modules.
- **Source References:** Retrieved document names and PDF page numbers are displayed where available.
- **Audit Logging:** Login, logout, and document upload/indexing outcomes are recorded in SQLite and displayed to Admin users.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | User interface |
| Google Gemini API | AI response generation |
| Gemini Embeddings | Document and query embeddings |
| ChromaDB | Vector database |
| SQLite | Authentication and audit records |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| LangChain | Text chunking and splitting |

Check `requirements.txt` for the project's installed package list.

## 3. Application Architecture

The application follows a document-processing and retrieval-augmented generation architecture.

### Document Ingestion Workflow

1. Admin uploads a PDF, DOCX, or TXT document.
2. The document processor extracts its text.
3. The text chunker divides the content into smaller sections.
4. Metadata is assigned, including category and access level.
5. Gemini generates document embeddings.
6. ChromaDB stores the indexed document chunks.
7. SQLite records the upload and indexing outcome in the audit log.

### Question Answering Workflow

1. A user submits a question through the Streamlit interface.
2. The advisor router identifies the appropriate advisor.
3. The relevant advisor retrieves authorized document chunks.
4. The advisor processes the retrieved information.
5. Gemini generates an answer where required.
6. The application displays the response and available source references.

### Specialized Advisors

| Advisor | Responsibility |
|---|---|
| General Advisor | General company knowledge and document questions using RAG and Gemini |
| Finance Advisor | Finance-related questions and calculation logic |
| HR Advisor | HR policy questions and relevant document retrieval |

If a question cannot be confidently classified as Finance or HR, it is routed to the General Advisor.

## 4. Project Structure

```text
NEXUS_AI/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── auth.py
│   ├── audit_log.py
│   └── nexus.db
│
├── modules/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── text_chunker.py
│   ├── embedding_manager.py
│   ├── vector_store.py
│   ├── rag_engine.py
│   ├── advisor_router.py
│   ├── finance_calculator.py
│   ├── finance_advisor.py
│   └── hr_advisor.py
│
├── data/
│   ├── documents/
│   └── chroma_db/
│
└── tests/
```

The structure represents the main project components. Additional files may exist as development continues.

## 5. Setup and Installation

### Prerequisites

- Python installed on your system.
- A valid Google Gemini API key.
- Internet access for Gemini API requests.

### Step 1: Clone the Repository

```bash
git clone https://github.com/alakanandakrishnanp2-source/NEXUS_AI.git
```

Navigate to the project directory:

```bash
cd NEXUS_AI
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory.

Add your own API credentials locally:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.8-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

The model values should match the models available to your Gemini API project.

**Security Note:** Never upload your `.env` file, API keys, passwords, or other credentials to GitHub.

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the application.

## 6. How to Use the Application

### Admin User

1. Log in using an Admin account configured in the application's authentication database.
2. Open Document Management.
3. Upload a PDF, DOCX, or TXT document.
4. Select its category: General, Finance, or HR.
5. Select its access level: Standard, Admin, or Public.
6. Submit the document.
7. The application automatically extracts text, creates chunks, generates embeddings, and indexes the document.
8. Review recent system activity through the Admin Dashboard.
9. Use the Knowledge Assistant to ask questions.

### Standard User

1. Log in using a Standard account.
2. Open the Knowledge Assistant.
3. Ask questions about available company documents.
4. The retrieval layer restricts access to documents marked Public or Standard and to the relevant advisor category.

## 7. Advisor Routing

The advisor router classifies incoming questions and directs them to one of three advisors:

- **General Advisor:** Handles general company knowledge and document questions using RAG and Gemini.
- **Finance Advisor:** Handles finance-related questions using indexed Finance documents and the project's calculation logic.
- **HR Advisor:** Handles HR policy questions using indexed HR documents.

Questions that cannot be confidently classified as Finance or HR are routed to General.

## 8. Access Control

The vector search layer applies role-based and category-based filters.

| User Role | Document Access |
|---|---|
| Admin | Documents across access levels |
| Standard | Public and Standard documents |

Advisor retrieval is also restricted to its configured document category.

Access checks should be enforced in the retrieval layer, not only through the user interface.

This proof-of-concept requires a separate security review before production deployment.

## 9. Audit Logging

The SQLite `audit_logs` table records application events, including:

- User login.
- User logout.
- Document upload and indexing success.
- Document upload and indexing failure.

The Admin Dashboard displays recent audit records, including:

- Username.
- Action.
- Document name.
- Category.
- Access level.
- Timestamp.
- Status.
- Details.

The current audit implementation is intended for demonstration purposes. Audit records are not tamper-proof and do not capture every possible security event.

## 10. Example Demonstration Questions

### General Advisor

- Give me a complete company overview of Nexus Technologies LLC.
- What are the core business activities of the company?
- How many employees work at the company?

### Finance Advisor

- What are the company's revenue, expenses, net profit, and profit margin?

### HR Advisor

- How many days of annual leave are provided?
- What is the process for submitting a leave request?

Use only synthetic or otherwise authorized sample documents during demonstrations.

## 11. Limitations and Future Improvements

This project is a time-boxed proof-of-concept rather than a production deployment.

Potential improvements include:

- Stronger authentication and authorization.
- Improved secret management.
- More comprehensive audit logging and retention.
- Improved retrieval quality and document metadata validation.
- Automated end-to-end testing.
- Better handling of API quota limits and service failures.
- Additional specialized AI advisors.
- Enterprise integrations and workflow automation.
- Secure cloud deployment and monitoring.

Gemini API availability and usage quotas may affect response generation.

## 12. Responsible AI and Security

- Use synthetic or approved documents for demonstrations.
- Never expose API keys, passwords, or confidential information in the repository.
- Verify AI-generated answers against their cited source documents.
- Do not treat generated responses as authoritative financial, HR, legal, or management decisions.
- Conduct appropriate security testing before production use.

## 13. AI Assistance Disclosure

AI tools were used to assist with parts of the development process, including code drafting, debugging support, prompt refinement, and documentation preparation.

The project implementation and demonstration should be reviewed and validated by the developer before submission.

---

**NEXUS AI – Executive Advisory & Intelligence Platform**

*An AI-powered approach to company knowledge management and specialized business advisory.*
