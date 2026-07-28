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
