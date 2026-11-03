NEXUS AI – Executive Advisory & Intelligence Platform
NEXUS AI is a proof-of-concept knowledge and advisory application for company documents. It allows authorized users to ask questions about indexed documents and provides specialized General, Finance, and HR advisory routes.
1. Implemented capabilities
- Authentication: login through the application's existing SQLite authentication module.
- Role-based document access: Admin and Standard roles are supported.
- Document management: Admin users can upload PDF, DOCX, and TXT files.
- Document processing: text extraction, chunking, metadata assignment, embedding generation, and indexing.
- Retrieval-augmented generation (RAG): the General Advisor retrieves authorized General-category document chunks and uses Gemini to generate an answer.
- Specialized advisors: Finance and HR questions are routed to their respective advisor modules.
- Source references: retrieved document names and PDF page numbers are displayed where available.
- Audit logging: login, logout, and document upload/indexing outcomes are recorded in SQLite and displayed to Admin users.
This is a demonstration proof-of-concept, not a production-ready enterprise system.
2. Technology stack
- Python
- Streamlit
- Google Gemini API (google-genai)
- Gemini embeddings (gemini-embedding-001, configured through the environment)
- ChromaDB for vector storage
- SQLite for authentication and audit records
- PyMuPDF for PDF text extraction
- python-docx for DOCX text extraction
- LangChain text splitters for chunking
Check requirements.txt for the project's installed package list.
3. Application architecture
                         User
                          |
                    Streamlit UI
                          |
                  Authentication
                    (SQLite)
                          |
                Role / Permission Check
                          |
             +------------+-------------+
             |                          |
       Admin Dashboard            Standard Dashboard
             |                          |
       Document Upload            Knowledge Assistant
             |
       Text Extraction
      (PDF / DOCX / TXT)
             |
        Text Chunking
             |
       Metadata Assignment
    (category / access level)
             |
      Gemini Embeddings
             |
        ChromaDB
             |
       Audit Log (SQLite)


     User Question -> Advisor Router
                          |
          +---------------+---------------+
          |               |               |
       General          Finance           HR
          |               |               |
    General RAG       Finance Logic     HR Policy
          |               |               |
       Gemini          Finance          HR
       + ChromaDB      Advisor          Advisor
          |               |               |
          +---------------+---------------+
                          |
                  Answer + Sources
                          |
                    Streamlit UI
4. Project structure
The main application files are organized as follows. The exact contents may vary as the project evolves.
NEXUS_AI/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── database/
│   ├── __init__.py
│   ├── auth.py
│   ├── audit_log.py
│   └── nexus.db
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
├── data/
│   ├── documents/
│   └── chroma_db/
└── tests/
Generated databases, uploaded documents, virtual environments, and secrets should not be committed to a public repository.
5. Setup and installation
Prerequisites
- Python installed
- A Google Gemini API key
- Internet access for Gemini API requests
Create and activate a virtual environment
Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1
Install dependencies
pip install -r requirements.txt
Configure environment variables
Create a .env file in the project root. Add your own valid API key locally:
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.6-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
Do not commit .env or share API keys in screenshots, source control, or assessment materials.
Run the application
streamlit run app.py
Open the local URL printed by Streamlit in your browser.
6. How to use
Admin
1. Log in with an Admin account configured in the application's authentication database.
2. Open Document Management.
3. Upload a PDF, DOCX, or TXT file.
4. Select its category: General, Finance, or HR.
5. Select its access level: Standard, Admin, or Public.
6. Submit the upload. The application extracts text, creates chunks, generates embeddings, and indexes the chunks.
7. Review recent system audit records in the Admin Dashboard.
8. Use the Knowledge Assistant to ask questions.
Standard user
1. Log in with a Standard account configured in the authentication database.
2. Ask questions through the Knowledge Assistant.
3. Retrieval is restricted to documents marked Public or Standard and to the relevant advisor category.
7. Advisor routing
The advisor router classifies incoming questions and directs them to one of three advisors:
- General Advisor: general company knowledge and document questions. It retrieves General-category documents and generates answers using Gemini.
- Finance Advisor: finance-related questions. The finance module uses the indexed Finance documents and the project's finance calculation logic.
- HR Advisor: HR-related questions. The HR module searches HR-category documents and extracts relevant policy information.
If a question cannot be confidently classified as Finance or HR, it is routed to General.
8. Access control
The vector search layer applies role and category filters:
- Standard users: can retrieve documents with public or standard access levels.
- Admin users: can retrieve documents across access levels.
- Category filter: advisor retrieval is restricted to its configured category.
Access checks must be enforced in the retrieval layer, not only hidden in the user interface. This proof-of-concept should receive a separate security review before production use.
9. Audit logging
The SQLite audit_logs table records application events, including:
- User login
- User logout
- Document upload and indexing success
- Document upload and indexing failure
The Admin Dashboard displays recent audit records, including username, action, document name, category, access level, timestamp, status, and details.

The current audit implementation is suitable for a demonstration. It is not tamper-proof and does not claim to capture every possible security event.
10. Example demonstration questions
General
- Give me a complete company overview of Nexus Technologies LLC.
- What are the core business activities of the company?
- How many employees work at the company?
Finance
- What are the company's revenue, expenses, net profit, and profit margin?
HR
- How many days of annual leave are provided?
- What is the process for submitting a leave request?
Use only the synthetic or otherwise authorized sample documents prepared for the demonstration.
11. Limitations and next steps
- This is a time-boxed proof-of-concept, not a production deployment.
- Authentication, authorization, audit retention, and secret management require further hardening.
- Audit records are stored in the application's SQLite database and are not tamper-proof.
- Retrieval quality depends on document quality, metadata accuracy, chunking, and embedding results.
- Gemini API availability and quotas can affect answer generation.
- Add automated tests for end-to-end upload, access control, advisor routing, and failure scenarios before production use.
12. Responsible AI and security
- Use synthetic or approved documents in the demonstration.
- Never place API keys, passwords, or confidential company information in the repository.
- Do not rely on generated answers without checking their cited source documents.
- The application is an advisory assistant and should not replace authorized financial, HR, legal, or management decisions.
13. AI assistance disclosure
AI tools were used to assist with parts of the development process, including code drafting, debugging support, prompt refinement, and documentation preparation. The project implementation and demonstration should be reviewed and validated by the developer before su
