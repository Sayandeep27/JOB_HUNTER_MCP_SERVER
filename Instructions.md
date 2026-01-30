# AI Job Recommender (Agent-Ready + UI-Driven)

An **industry-grade AI Job Recommendation system** that analyzes a resume, identifies skill gaps, generates a career roadmap, and fetches **real-time jobs from LinkedIn & Naukri**.

The project is designed in **two modes**:

* **User-facing UI** (Streamlit)
* **Agent-facing tool server** (MCP – Model Context Protocol)

This makes it usable by **humans and AI agents** alike.

---

## 🚀 Key Highlights

* Resume parsing from PDF
* LLM-powered resume summarization
* Skill gap analysis
* Career roadmap generation
* Intelligent job-search keyword extraction
* Real job listings (LinkedIn + Naukri via Apify)
* MCP-based tool server for agentic workflows
* Clean, modular, production-ready architecture

---

## 🧠 Tech Stack

| Layer           | Technology                       |
| --------------- | -------------------------------- |
| Frontend        | Streamlit                        |
| LLM             | Groq (LLaMA-3.1-8B-Instant)      |
| Resume Parsing  | PyMuPDF                          |
| Job Data        | Apify (LinkedIn & Naukri actors) |
| Agent Interface | MCP (FastMCP)                    |
| Language        | Python                           |

---

## 📁 Project Structure

```text
project-root/
│
├── app.py                # Streamlit UI (user-facing app)
├── mcp_server.py         # MCP tool server (agent-facing)
│
├── src/
│   ├── helper.py         # PDF parsing + LLM utilities
│   └── job_api.py        # Real job fetching via Apify
│
├── .env                  # API keys
├── requirements.txt
└── README.md
```

---

## 1️⃣ `mcp_server.py` — MCP Tool Server

### Purpose

This file exposes **job-fetching logic as AI-callable tools** using MCP.

These tools can be used by:

* Claude Desktop
* LangGraph / AutoGPT-style agents
* Any MCP-compatible LLM client

Think of this as:

> **Backend job APIs that AI agents can invoke**

---

### MCP Server Initialization

```python
from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

mcp = FastMCP("Job Recommender")
```

* Creates an MCP server named **Job Recommender**
* This name appears inside MCP clients

---

### MCP Tool: LinkedIn Jobs

```python
@mcp.tool()
async def fetchlinkedin(listofkey):
    return fetch_linkedin_jobs(listofkey)
```

* Registers a tool named `fetchlinkedin`
* Accepts job keywords
* Calls Apify LinkedIn actor internally
* Returns structured job data

---

### MCP Tool: Naukri Jobs

```python
@mcp.tool()
async def fetchnaukri(listofkey):
    return fetch_naukri_jobs(listofkey)
```

* Same concept
* Different data source

---

### MCP Server Execution

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

* Runs MCP over **STDIO**
* Required for Claude Desktop MCP integration
* **Not used by Streamlit**

---

### Key Takeaway

> MCP server = **AI-agent interface** to your job APIs

It is optional for UI apps but powerful for:

* Agentic AI
* Tool-calling LLMs
* Multi-step reasoning pipelines

---

## 2️⃣ `app.py` — Streamlit Frontend (UI)

### Purpose

This is the **user-facing application** where:

* Users upload resumes
* LLM analyzes resumes
* Jobs are fetched and displayed visually

---

### Core Imports

```python
import streamlit as st
from src.helper import extract_text_from_pdf, ask_groq
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs
```

* `helper.py` → PDF + LLM logic
* `job_api.py` → Real job data

**Important:** Streamlit directly calls APIs — **no MCP involved**

---

### Resume Upload

```python
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
```

* Accepts PDF resumes
* Triggers the entire AI pipeline

---

### Resume Processing Pipeline

#### 1. Text Extraction

```python
resume_text = extract_text_from_pdf(uploaded_file)
```

* Uses PyMuPDF
* Reads PDF from memory
* Extracts raw resume text

---

#### 2. Resume Summary (LLM)

```python
summary = ask_groq("Summarize this resume...")
```

* Extracts skills, education, experience

---

#### 3. Skill Gap Analysis

```python
gaps = ask_groq("Analyze this resume and highlight missing skills...")
```

* Identifies missing tools, certifications, experience

---

#### 4. Career Roadmap

```python
roadmap = ask_groq("Suggest a future roadmap...")
```

* Learning path
* Career growth suggestions

---

### Job Recommendation Flow

#### Keyword Extraction (LLM)

```python
keywords = ask_groq("Suggest best job titles and search keywords...")
```

* Converts resume → optimized job-search keywords

Example:

> Data Scientist, Machine Learning Engineer, Python, NLP

---

#### Job Fetching

```python
linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean)
naukri_jobs = fetch_naukri_jobs(search_keywords_clean)
```

* Fetches **real-time jobs**
* No scraping logic written manually

---

### Job Display

Each job card shows:

* Job title
* Company
* Location
* Apply link

---

## 3️⃣ `helper.py` — PDF + LLM Utilities

### Purpose

Centralized utilities for:

* PDF reading
* LLM interaction
* Environment handling

---

### Environment Setup

```python
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

* Secure API key handling

---

### Groq Client

```python
client = Groq(api_key=GROQ_API_KEY)
```

* Uses LLaMA-3.1-8B-Instant

---

### PDF Text Extraction

```python
def extract_text_from_pdf(uploaded_file):
```

* Uses PyMuPDF
* Reads uploaded PDF in memory
* Concatenates page text

---

### LLM Wrapper

```python
def ask_groq(prompt, max_tokens=500):
```

* Single reusable LLM function
* Controlled temperature
* Plain-text output

Used for:

* Summary
* Skill gaps
* Roadmap
* Job keywords

---

## 4️⃣ `job_api.py` — Real Job Data (Apify)

### Purpose

Fetch **real jobs** without manual scraping.

Sources:

* LinkedIn
* Naukri

---

### Apify Setup

```python
apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
```

* Uses Apify actors
* Handles proxies & rate limits

---

### LinkedIn Jobs

```python
def fetch_linkedin_jobs(search_query, location="india", rows=60):
```

* Calls LinkedIn Apify actor
* Returns structured JSON

---

### Naukri Jobs

```python
def fetch_naukri_jobs(search_query, location="india", rows=60):
```

* Similar flow
* Different data source

---

## 5️⃣ Overall Architecture

```text
User (Streamlit UI)
      ↓
Resume PDF
      ↓
PyMuPDF (Text Extraction)
      ↓
Groq LLM (Summary, Gaps, Roadmap)
      ↓
Groq LLM (Job Keywords)
      ↓
Apify (LinkedIn + Naukri)
      ↓
Job Cards in UI
```

---

## 6️⃣ Where MCP Fits (Critical Concept)

| Component        | Uses MCP |
| ---------------- | -------- |
| Streamlit UI     | ❌        |
| MCP Server       | ❌ UI     |
| Claude Desktop   | ✅        |
| LangGraph Agents | ✅        |

You intentionally built **both**:

* UI-based application
* Agent-ready tool server

This is **production-level architecture**.

---

## 7️⃣ Why This Is a Strong Project

* Uses **real job data** (not mock APIs)
* End-to-end resume intelligence
* Career guidance + skill gaps
* Agent-ready via MCP
* LLM-powered job search
* Clean separation of concerns
* Scales to multi-agent workflows

---

## 🏁 Final Note

This project mirrors **how modern AI products are actually built**:

* Humans interact via UI
* AI agents interact via tools
* Same backend logic serves both

If you want to extend this:

* Add job ranking
* Add resume scoring
* Add recruiter-style feedback
* Add LangGraph orchestration

You’re already very close to a **startup-grade AI system**.
