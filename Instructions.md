# 🧩 What Is This Project Actually Doing?

This project is a **professionally designed AI system** with a clean separation between **core logic**, **human-facing UI**, and **agent-facing APIs**.

At a high level, you built **ONE system with TWO entry points**:

* 🧑‍💻 **A normal user application (Streamlit)**
* 🤖 **An AI-agent tool server (MCP)**

Both entry points **share the same core engine**, but they are meant for **different consumers**.

---

## 🧠 Big Picture Architecture

```
              ┌────────────┐
              │ job_api.py │  ← core business logic
              └────────────┘
                     ▲
                     │
       ┌─────────────┴─────────────┐
       │                           │
┌────────────┐             ┌──────────────┐
│ Streamlit  │             │ MCP Server   │
│  app.py    │             │ mcp_server.py│
└────────────┘             └──────────────┘
       │                           │
       ▼                           ▼
    End User                AI / Agent
```

**Key idea:**

> The core logic does not care *who* is calling it — a human or an AI agent.

---

## 🧱 Step 0: Core Business Logic (The Foundation)

Before UI, before MCP, ask one question:

> **Where is the real work happening?**

### ✅ Answer

```
src/
 ├── job_api.py
 └── helper.py
```

These two files are the **engine of the entire system**.

Everything else is just an **interface** on top.

---

## 🔹 job_api.py — “Get Me Real Jobs”

### What this file does

* Connects to **Apify**
* Fetches **real job listings** from:

  * LinkedIn
  * Naukri
* Returns **structured JSON data**

### Example

**Input**

```
"data scientist python"
```

**Output**

```json
[
  {
    "title": "Data Scientist",
    "company": "ABC Corp",
    "location": "Bangalore",
    "link": "https://..."
  }
]
```

### What it does NOT care about

* ❌ Streamlit
* ❌ MCP
* ❌ LLMs

This makes it **fully reusable** anywhere.

---

## 🔹 helper.py — “Talk to LLMs & Read PDFs”

### What this file does

* Extracts text from **resume PDFs** (PyMuPDF)
* Talks to **Groq LLM**
* Returns **plain text responses**

### Responsibilities

* Resume text extraction
* Resume summarization
* Skill gap analysis
* Career roadmap generation
* Keyword extraction for job search

### What it does NOT contain

* ❌ Streamlit UI code
* ❌ MCP logic

Just **pure utilities**.

---

## ✅ These Two Files = Your Engine

Everything else:

* UI
* APIs
* Agents

are just **different ways of using the same engine**.

---

## 🧱 Step 1: Streamlit App (Human Interface)

This is the part **users actually see**.

### How it runs

```
streamlit run app.py
```

📌 Important:

> When Streamlit runs, **MCP does NOT run**.

---

## 🔹 Step 1.1: Resume Upload

```python
uploaded_file = st.file_uploader(...)
```

User uploads a **PDF resume**.

---

## 🔹 Step 1.2: Resume Text Extraction

```python
resume_text = extract_text_from_pdf(uploaded_file)
```

**Flow**

```
PDF → PyMuPDF → Raw Text
```

---

## 🔹 Step 1.3: Resume Summarization (LLM)

```python
summary = ask_groq("Summarize this resume...")
```

**Flow**

```
Resume Text → Groq LLM → Summary
```

---

## 🔹 Step 1.4: Skill Gap Analysis (LLM)

```python
gaps = ask_groq("Highlight missing skills...")
```

**Flow**

```
Resume Text → Groq LLM → Missing Skills
```

---

## 🔹 Step 1.5: Career Roadmap (LLM)

```python
roadmap = ask_groq("Suggest future roadmap...")
```

**Flow**

```
Resume Text → Groq LLM → Career Plan
```

---

## 🔹 Step 1.6: Job Recommendation Button

Nothing happens automatically.

👉 **Jobs are fetched ONLY when the user clicks the button**.

---

### Step 1.6.1: Extract Job Keywords (LLM)

```python
keywords = ask_groq("Suggest job titles & keywords...")
```

**Example Output**

```
Data Scientist, Machine Learning Engineer, Python, NLP
```

---

### Step 1.6.2: Fetch Jobs

```python
linkedin_jobs = fetch_linkedin_jobs(keywords)
naukri_jobs = fetch_naukri_jobs(keywords)
```

**Flow**

```
Keywords → Apify → LinkedIn + Naukri → Jobs
```

---

### Step 1.6.3: Display Jobs

Streamlit loops through the results and renders **job cards** in the UI.

---

## ✅ This Is the Full Streamlit Flow

End-to-end, nothing hidden.

---

## 🧱 Step 2: MCP Server (Agent Interface)

This is where most confusion happens.

### ❓ Is MCP running when Streamlit runs?

❌ **NO**

They are completely independent.

---

## 🔹 What Is mcp_server.py?

It is a **separate program**.

### How it runs

```
python mcp_server.py
```

---

## 🔹 What Happens When MCP Runs?

* Starts an **MCP tool server**
* Registers tools:

  * `fetchlinkedin`
  * `fetchnaukri`
* Waits for an MCP client

That’s it.

---

## ❌ What MCP Server Does NOT Do

* ❌ No UI
* ❌ No resume analysis
* ❌ No LLM calls
* ❌ No automatic job fetching

It just **exposes tools**.

---

## 🧱 Step 3: Who Calls the MCP Server?

### Right now?

👉 **Nobody**.

You do **not** have an MCP client yet.

---

## 🔮 Possible Future MCP Clients

| Client                 | Role                |
| ---------------------- | ------------------- |
| Claude Desktop         | Calls tools via MCP |
| LangGraph Agent        | Uses MCP tools      |
| Custom `mcp_client.py` | Manual tool calls   |

---

## 🔁 Example Future MCP Flow

```
Claude: "Find jobs for data scientist"
   ↓
Claude MCP Client
   ↓
mcp_server.py
   ↓
fetchlinkedin()
   ↓
Apify
```

---

## 🧠 Why Adding MCP Was a Smart Move

You accidentally did something **very professional**.

You separated:

* ✅ Business logic
* ✅ User interface
* ✅ Agent interface

This is **exactly** how real AI platforms are built.

---

## 🎯 Final Mental Model (Memorize This)

* **Streamlit app** → for humans
* **MCP server** → for AI agents
* **Core logic** → shared by both

📌 **Right now:**

> Only Streamlit is actively being used.

---

## 🏁 One-Line Summary

> **Streamlit app is for humans. MCP server is for AI agents. Core logic powers both.**

---

✨ You didn’t just build a project — you built a **scalable AI system architecture**.
