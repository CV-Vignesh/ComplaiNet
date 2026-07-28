# 🛡️ ComplaiNet - AI-Powered Pharmaceutical QMS

An enterprise-grade, AI-driven Quality Management System (QMS) designed to automate, analyze, and triage pharmaceutical customer complaints with unprecedented speed and accuracy.

Built as a comprehensive internship assessment project, ComplaiNet leverages cutting-edge LLMs and strict medical compliance rules to transform raw, unstructured complaint data (emails, PDFs, Word docs) into structured, highly actionable QA insights.

## ✨ Key Features

- **🧠 Groq-Powered AI Copilot**: Instantly extracts and structures complaint data from messy emails, raw text, and documents using ultra-fast LLM inference via LangGraph.
- **⚕️ ICH Q10 Risk Assessment**: Automatically evaluates complaints against ICH Q10 pharmaceutical quality system guidelines to determine Initial Severity, Priority, CAPA (Corrective and Preventive Action) requirements, and Regulatory Reportability.
- **🔍 Advanced Duplicate Detection**: Features a rigorous 10-field exact-match algorithm that instantly cross-references the PostgreSQL database to flag duplicate reports while intelligently avoiding false positives on form edits.
- **📊 Completeness & Quality Scoring**: Calculates a real-time Completeness Score (0-100%) and alerts QA agents to any critical missing information (e.g., missing batch numbers or expiry dates).
- **🎨 Glassmorphic Enterprise UI**: A beautiful, highly responsive, and modern React dashboard built with Vite, utilizing Redux for seamless state management and instant AI conversation rendering.
- **☁️ Supabase PostgreSQL Integration**: Secure, cloud-hosted relational data storage utilizing SQLAlchemy for robust backend ORM.

## 🛠️ Technology Stack

**Frontend:**
- React (Vite)
- Redux (State Management)
- Lucide React (Iconography)
- Vanilla CSS (Bespoke Glassmorphism Design System)

**Backend:**
- Python (FastAPI)
- LangChain / LangGraph (AI Orchestration)
- Groq API (High-speed LLM Inference)
- SQLAlchemy (Database ORM)
- python-docx & pdfplumber (Document Parsing)

**Database:**
- PostgreSQL (Hosted on Supabase)

## 🚀 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/complaiNet.git
cd complaiNet
```

### 2. Backend Setup (FastAPI)
Navigate to the backend directory and set up your virtual environment:
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```
**Environment Variables (`.env`)**:
You must create a `.env` file in the `backend/` directory with the following keys:
```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://your_supabase_url_here
```
Run the FastAPI server:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup (React/Vite)
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```
The frontend will launch at `http://localhost:5173/`.

## 🧪 Testing the AI Engine

The repository comes with a comprehensive suite of 32 test cases (in `.eml`, `.docx`, and `.txt` formats) designed to showcase the AI's capabilities. 

To test the system:
1. Open the ComplaiNet web dashboard.
2. Drag and drop any of the provided test files from the `Tests/` directory directly into the AI Chat Panel.
3. Watch as the AI parses the document, extracts the data, assigns a completeness score, and maps the ICH Q10 risk assessment in real-time!

---
*Built with passion for next-generation pharmaceutical quality assurance.*

# 🛡️ ComplaiNet - AI-Powered Pharmaceutical QMS

An intelligent Quality Management System (QMS) designed to automate, analyze, and triage pharmaceutical customer complaints with speed and accuracy. 

Built as an advanced AI engineering project, ComplaiNet transforms raw, unstructured complaint data (emails, PDFs, Word docs) into structured, highly actionable Quality Assurance (QA) insights.

## ✨ Key Features

- **🧠 AI Copilot**: Instantly extracts and structures complaint data from messy emails and raw text using ultra-fast LLM inference.
- **⚕️ Medical Risk Assessment**: Automatically evaluates complaints against strict pharmaceutical quality system guidelines to determine Severity, Priority, CAPA (Corrective and Preventive Action) requirements, and Regulatory Reportability.
- **🔍 Advanced Duplicate Detection**: Features a rigorous 10-field exact-match algorithm that instantly cross-references the database to flag duplicate reports while intelligently avoiding false positives on user edits.
- **📊 Completeness Scoring**: Calculates a real-time Completeness Score (0-100%) and alerts QA agents to any critical missing information (e.g., missing batch numbers or expiry dates).
- **🎨 Modern Enterprise UI**: A beautiful, highly responsive React dashboard built with Vite and Redux.

## 🛠️ Technology Stack

- **Frontend:** React, Vite, Redux, Vanilla CSS Glassmorphism
- **Backend:** Python, FastAPI, LangGraph, Groq API (LLM Inference)
- **Database:** PostgreSQL (Hosted on Supabase), SQLAlchemy ORM

## 🚀 Local Setup & Installation

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/yourusername/complaiNet.git
cd complaiNet
\`\`\`

### 2. Backend Setup
Navigate to the backend directory, set up your virtual environment, and install dependencies:
\`\`\`bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

Create a `.env` file in the `backend/` directory with your keys:
\`\`\`env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://your_supabase_url_here
\`\`\`

Run the server:
\`\`\`bash
uvicorn main:app --reload
\`\`\`

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory:
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`
The frontend dashboard will launch at `http://localhost:5173/`.
