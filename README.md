# Agentic AI with LangGraph & Model Context Protocol (MCP)

This repository contains learning projects, notebooks, and source code covering the fundamentals I learnt and implemented of building stateful, multi-actor LLM applications using **LangGraph** and extending model capabilities using the **Model Context Protocol (MCP)**.

---

## 🚀 What I Learned & Implemented

### 1. LangGraph Fundamentals (`1-BasicChatbot`)
In the [`1-BasicChatbot/1-basicchatbot.ipynb`](./1-BasicChatbot/1-basicchatbot.ipynb) notebook, I built and understood the core components of LangGraph:
* **StateGraph Architecture**: How to design cyclical graphs where nodes (actions/LLM calls) and edges (transitions) communicate via a shared central `State` object.
* **Reducers**: Used `add_messages` to manage and append list-based conversation histories in the state rather than overwriting them.
* **Graph Visualization**: Visualized workflows dynamically by compiling graphs and drawing Mermaid PNG diagrams.
* **ReAct Agent Architecture**: Built reasoning loops using tools (custom python math tools and Tavily Search API) with conditional routing logic (`should_continue`).
* **Graph Memory & Checkpointing**: Integrated `MemorySaver` to retain conversation memory across different sessions using `thread_id` configurations.
* **Streaming Modes**: Explored different streaming strategies in LangGraph (updates vs. values) to stream execution states and model responses in real-time.

### 2. Model Context Protocol (MCP) with LangChain (`mcplangchain`)
Inside the [`mcplangchain`](./mcplangchain) folder, I implemented a modular MCP architecture containing custom tools served over different transports:
* **Math Server (`mathserver.py`)**: A `FastMCP` server utilizing **stdio** transport to register `add` and `multiply` tools.
* **Weather Server (`weather.py`)**: A `FastMCP` server utilizing **streamable-http** transport acting like an API server for a `get_weather` tool.
* **Multi-Server MCP Client (`client.py`)**: 
  * Configured a `MultiServerMCPClient` to connect simultaneously to both the stdio and HTTP-based servers.
  * Discovered and retrieved tools dynamically from both servers.
  * Passed the tools into a LangChain ReAct agent powered by Groq's LLM (`llama-3.3-70b-versatile`).

---

## 🛠️ Tech Stack & Dependencies
* **Frameworks**: LangGraph, LangChain, FastMCP
* **LLM Provider**: ChatGroq (Llama 3.3 70B Versatile)
* **APIs**: Tavily Search Engine, Google Gemini API, OpenAI API
* **Environment Management**: `dotenv` for secure environment variable loading
* **Package Manager**: `uv` / `pip` (`requirements.txt`, `pyproject.toml`)

## ⚙️ How to Setup & Run the Project

Follow these steps to set up the project on your local machine and run the notebooks and MCP servers:

### 1. Clone the Repository
Open your terminal (Git Bash, Command Prompt, or terminal of your choice) and run:
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd AgenticLanggraph
```

### 2. Set Up a Python Virtual Environment
Initialize a virtual environment to keep dependencies isolated:
```bash
python -m venv .venv
```
Activate the virtual environment:
* **Windows (Git Bash):**
  ```bash
  source .venv/Scripts/activate
  ```
* **Windows (Command Prompt / PowerShell):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Project Dependencies
Use `pip` to install all required packages:
```bash
pip install -r requirements.txt
```
*(Alternatively, if you use the `uv` tool, you can run `uv pip install -r requirements.txt` or `uv sync` to sync with the `uv.lock` file).*

### 4. Configure Environment Variables
Create your local `.env` file by copying the template:
```bash
cp .env.example .env
```
Open the newly created `.env` file and insert your actual API keys:
```env
GROQ_API_KEY="your-groq-api-key"
TAVILY_API_KEY="your-tavily-api-key"
GOOGLE_API_KEY="your-google-api-key"
OPENAI_API_KEY="your-openai-api-key"
```

### 5. Running the Jupyter Notebooks
To run the LangGraph chatbot tutorial notebook:
1. Start Jupyter:
   ```bash
   jupyter notebook
   ```
2. Navigate to and open `1-BasicChatbot/1-basicchatbot.ipynb`.
3. Run the cells step-by-step to build the chatbot, add tools, enable memory checkpointers, and view the Mermaid flowcharts.

### 6. Running the Model Context Protocol (MCP) Demo
The MCP demo requires running the weather server first and then the client:
1. **Start the Weather Server** (runs over HTTP):
   ```bash
   python mcplangchain/weather.py
   ```
   *Keep this terminal running (it listens at `http://localhost:8000/mcp`).*

2. **Run the Client** (runs in a new terminal with the virtual environment activated):
   ```bash
   python mcplangchain/client.py
   ```
   *The client will start the math server internally via standard I/O (stdio), fetch tools from both servers, and query the Llama model on Groq to answer questions.*
