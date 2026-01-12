# Project Documentation: HEPHAESTUS – Intelligent Financial Advisor

## 1. Context & Objectives

**Project Name:** IA BOT – Agent conversationnel Intelligent (Project HEPHAESTUS)  
**Timeline:** January 8th to January 16th, 2026  

### Core Goal
Design a functional prototype of an intelligent conversational agent integrated into a web application.

### User Persona
Young investors seeking guidance to start their investment journey.

### Functional Perimeter
The agent must:
- Understand natural language queries  
- Execute real-time web scraping  
- Provide live financial data  

---

## 2. Global Architecture

The project relies on a **modular agentic architecture** designed for local execution.

### 2.1 Technical Stack

| Layer        | Technology                 | Role |
|--------------|----------------------------|------|
| Frontend     | JavaScript / TypeScript    | User interface and interaction with the chatbot |
| Backend      | Python (FastAPI / Flask)   | Orchestrator, managing MCP, tooling, and LLM integration |
| LLM Runtime  | Ollama                     | Local deployment of the open-source model |
| Model        | Phi 3.5 Mini               | Reasoning engine for natural language and tool selection |
| MCP Server   | Python                     | Implementation of the Model Context Protocol to bridge the LLM and tools |
| Tooling      | n8n (Local Docker)         | Specialized engine for real-time Yahoo Finance scraping |

---

## 3. Component Details

### 3.1 Frontend (The Client)

- **Interface:** A professional “site vitrine” focused on financial education  
- **Chatbot:** A dedicated chat window for natural language interaction  
- **Communication:** Interaction with the Python backend via secure protocols to display live data  

---

### 3.2 Backend & MCP (The Brain)

- **Orchestration:** The backend manages the flow between the user, the LLM, and the tools  
- **MCP Integration:** A Python-based MCP server simulates the integration of external tools  
- **Reasoning:** The LLM (Phi 3.5) analyzes queries and decides when to trigger the scraping tool to avoid hallucinations  

---

### 3.3 Scraping Logic (n8n & Yahoo Finance)

- **Implementation:** n8n is used as a local service to perform real-time scraping  
- **Data Source:** Live extraction of stock prices, trends, and news from Yahoo Finance  

#### Ethics & Compliance
- Targeting public data only (no authentication or paywalls)  
- Low-frequency requests to avoid server spam  
- Respect for `robots.txt` and website terms of use  

---

## 4. Operational Data Flow

1. **Request:** User asks: *“Should I buy Apple (AAPL) stock today?”*  
2. **Analysis:** The Python backend sends the query to Phi 3.5 via Ollama  
3. **Decision:** The LLM determines it needs current market data and calls the `get_market_data` tool via the MCP  
4. **Action:**  
   - The MCP server triggers a local n8n webhook  
   - n8n scrapes Yahoo Finance and returns a JSON payload  
5. **Synthesis:**  
   - The LLM receives the real data  
   - Analyzes it  
   - Provides a formatted financial advice response to the frontend  

---

## 5. Constraints & Deliverables

### Constraints
- **Local Execution:** Mandatory use of a local open-source model  
- **No Paid APIs:** No paid API keys allowed  
- **No Mock Data:** The system must perform real, functional scraping  

### Final Deliverables
- A functional web application combining the site and the chatbot  
- Technical documentation explaining architecture, data flow, and technology choices  
- A 20-minute defense including a live demonstration and critical analysis  
