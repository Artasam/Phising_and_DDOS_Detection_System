## 🛡️ Phishing & DDoS Detection Agent

Hybrid cybersecurity assistant that detects **phishing emails** and **DDoS traffic** using:

- **Rule-based heuristics** (URL, attachment, text and traffic patterns)
- **External threat intel** via **VirusTotal**
- **Groq LLM (Llama 3.3 70B)** for final, human-readable reasoning
- **LangGraph** to orchestrate the workflows
- A modern **Streamlit dashboard** for interactive analysis

---

### 1. Project Overview

- **Phishing detection**  
  - Checks URLs (optionally via VirusTotal), attachments, and email text.  
  - Uses simple rules to flag suspicious signals.  
  - Sends aggregated indicators to an LLM, which returns a concise decision and explanation.

- **DDoS detection**  
  - Ingests basic HTTP traffic logs (IPs, path, packet size, rate, user-agent).  
  - Extracts features and applies rule-based logic to flag abnormal traffic.  
  - Runs an LLM “SOC analyst” on the raw log to validate the verdict and explain why.

The Streamlit UI exposes both workflows in a **single security dashboard** that is suitable to demo to recruiters or stakeholders.

---

### 2. Tech Stack

- **Python**
- **LangGraph** – graph-based orchestration of the phishing and DDoS flows  
- **LangChain + langchain_groq** – LLM integration with Groq
- **Groq API** – `llama-3.3-70b-versatile` model for security reasoning
- **Streamlit** – interactive web UI  
- **Requests** – VirusTotal API calls  
- **python-dotenv** – local environment management

---

### 3. Repository Structure (key files)

- `app.py` – Streamlit dashboard (Phishing & DDoS tabs, UX, secrets handling)
- `main.py` – minimal script demo for the phishing flow
- `workflows/langgraph_phishing_flow.py` – LangGraph graph for phishing detection
- `workflows/langgraph_ddos_flow.py` – LangGraph graph for DDoS detection
- `agents/phishing_agent.py` – combines VirusTotal, attachment and text checks
- `agents/ddos_agent.py` – CLI-style DDoS runner over sample traffic
- `tools/traffic_analyzer.py` – feature extraction from raw traffic logs
- `tools/dos_rules.py` – rule-based DDoS detection
- `tools/llm_explainer.py` – Groq LLM wrapper for DDoS reasoning
- `tools/vt_checker.py` – VirusTotal URL analysis helper
- `tools/attachment_checker.py` – attachment filename heuristics
- `tools/rule_engine.py` – basic text-based phishing heuristics
- `data/sample_traffic.json` – sample HTTP traffic logs for DDoS testing

---

### 4. Setup

#### 4.1. Clone and install

```bash
git clone <your-repo-url>
cd Phishing-and-Ddos-Detection-Agent
pip install -r requirements.txt
```

#### 4.2. Environment variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
VT_API_KEY=your_virustotal_api_key_here  # optional but recommended
```

- `GROQ_API_KEY` – **required** for all LLM calls (Groq).
- `VT_API_KEY` – **optional**; used for VirusTotal URL checks in phishing detection.

In **Streamlit Cloud** (or other hosted environments), you can configure these as `st.secrets` instead of a `.env` file:

- `GROQ_API_KEY`
- `VT_API_KEY` (optional)

The app will first try `st.secrets` and fall back to `.env` when running locally.

---

### 5. Running the Streamlit Dashboard

From the project root:

```bash
streamlit run app.py
```

You’ll see a two-tab interface:

- **“✉️ Phishing” tab**
  - Inputs: `URL`, `Attachment filename`, `Email body text`.
  - Output:
    - LLM decision (e.g. “This is likely a phishing email because …”)
    - Indicator summary (URL / attachment / text flags).

- **“🌐 DDoS” tab**
  - Inputs: `Source IP`, `Destination IP`, `Timestamp`, `Request type`, `Path`, `Packet size`, `Rate per minute`, `User-Agent`.
  - Output:
    - High-level verdict: DDoS detected vs normal traffic.
    - Rule-based explanation (which heuristics triggered).
    - LLM explanation (SOC-style reasoning).
    - Full log payload for inspection.

The UI uses a custom dark theme, gradient highlights, and card-based layout to feel like a modern SOC dashboard for demos.

---

### 6. How It Works (High Level)

#### Phishing Flow

1. `phishing_agent`:
   - Checks URL with VirusTotal (via `vt_checker`) if possible.
   - Flags suspicious attachment names and email wording (rules).
   - Returns a `results` dict with individual flags.
2. `langgraph_phishing_flow`:
   - LangGraph node aggregates `results`.
   - LLM node (`ChatGroq`) receives a short prompt summarizing indicators.
   - Produces a final **decision** string with reasoning.

#### DDoS Flow

1. `traffic_analyzer.extract_features` builds structured features from a raw log.
2. `dos_rules.is_ddos_attack` applies thresholds and heuristics.
3. `llm_explainer.llm_ddos_detector` queries Groq with the full log and parses the answer.
4. `langgraph_ddos_flow` merges rule + LLM signals into a single `result` object used by the UI.

---

### 7. Example: CLI Demos (Optional)

Run the DDoS agent over sample traffic:

```bash
python agents/ddos_agent.py
```

Run the phishing demo script:

```bash
python main.py
```

---

### 8. Ideas for Extension

- Add **persistence/logging** of decisions (e.g. to a DB or CSV).
- Integrate authentication around the Streamlit app for multi-user use.
- Expand phishing signals (SPF/DKIM/DMARC headers, sending domain reputation).
- Add more traffic features (TCP flags, geoIP, ASN) for richer DDoS detection.



# 🛡️ AI Threat Detection Agent – Powered by LangGraph + Groq

This project is a lightweight **AI-powered cyber threat detection pipeline** built using **LangGraph**, **Groq LLMs**, and **external tools** like **VirusTotal**.
It supports **real-time phishing email analysis** as well as **DDoS traffic pattern detection** using a hybrid rule + LLM approach.

---

## 🚨 What It Detects

* 🕵️ **Phishing Emails**

  * Malicious URLs
  * Dangerous file attachments
  * Suspicious keywords or phrases

* 🌐 **DDoS Attacks**

  * High-rate, large-packet network traffic
  * Automated bot behavior
  * LLM-assisted traffic analysis and explanation

---

## 🚀 Key Features

* ✅ **Modular Agents**: Each agent handles a specific task (phishing or DDoS)
* 🔄 **LangGraph StateFlow**: Directs how agents process inputs
* 🧠 **LLM Reasoning**: Uses Groq's Mixtral/LLama3 via LangChain for context-aware analysis
* 🔗 **VirusTotal Integration**: For real-time phishing URL threat scoring

---

## 📁 Project Structure

```
cyber_ai_soc/
├── agents/
│   ├── phishing_agent.py          # Phishing logic
│   └── ddos_agent.py              # DDoS logic (rule + LLM)
│
├── tools/
│   ├── vt_checker.py              # VirusTotal scanner
│   ├── attachment_checker.py      # Flags risky file types
│   ├── rule_engine.py             # Phishing keyword rules
│   ├── traffic_analyzer.py        # Extracts traffic features
│   ├── ddos_rules.py              # Rule-based DDoS detection
│   └── llm_explainer.py           # Groq LLM-based DDoS explanation
│
├── workflows/
│   ├── langgraph_phishing_flow.py # LangGraph flow for phishing
│   └── langgraph_ddos_flow.py     # LangGraph flow for DDoS
│
├── data/
│   └── sample_traffic.json        # Sample DDoS traffic logs
│
├── main.py                        # Unified entry to test both agents
├── .env                           # API keys (Groq + VirusTotal)
├── requirements.txt               # All dependencies
└── README.md                      # This file
```

---

## 🧠 How It Works

### 🟪 Phishing Detection Pipeline

1. **Input**: A suspicious email log with URL, attachment, and message text
2. **Tools**:

   * `vt_checker.py`: Checks URL via VirusTotal API
   * `attachment_checker.py`: Flags `.exe`, `.html`, etc.
   * `rule_engine.py`: Detects phishing keywords like `urgent`, `verify`
3. **LLM Reasoning**:

   * Groq LLM evaluates all signals to confirm if phishing
4. **LangGraph** coordinates the flow and final verdict

---

### 🟥 DDoS Detection Pipeline

1. **Input**: JSON traffic logs with IPs, rates, sizes, etc.
2. **Tools**:

   * `traffic_analyzer.py`: Extracts request type, size, rate
   * `ddos_rules.py`: Flags high-rate + bot-like behavior
   * `llm_explainer.py`: Groq LLM detects deeper pattern from log
3. **LangGraph** flow and `ddos_agent.py` combine both methods for final decision

---

## 🌐 API Keys Setup

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_groq_key_here
VT_API_KEY=your_virustotal_key_here
```

---

## 📦 Installation & Usage

```bash
# Step 1: Clone the repo
git clone https://github.com/yasirwali1052/Phishing-Detection-Agent.git
cd Phishing-Detection-Agent

# Step 2: Set up virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
# or
source venv/bin/activate # On Linux/Mac

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Add your .env file

# Step 5: Run either detection mode
python agents/phishing_agent.py        # For phishing detection
python agents/ddos_agent.py            # For DDoS detection
python workflows/langgraph_ddos_flow.py # LangGraph flow
```

Or run all via:

```bash
python main.py
```

---


---

## 👤 Author

**Artasam in Rashid**
📍 NUML Islamabad | B.S. in AI
🌐 [GitHub](https://github.com/Artasam)
💼 [LinkedIn](https://www.linkedin.com/in/artasam-bin-rashid-46258a315/)


