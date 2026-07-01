# Local Persian AI Agent CLI (`ollama-local-agent-cli`) 
A lightweight, production-ready Python command-line utility showcasing how to orchestrate local open-source Large Language Models (LLMs) via **Ollama**.

This project demonstrates how to ingest local model registries into structured data frames, implement token-by-token response streaming, and inject complex, domain-specific Persian system guidelines for automated enterprise helpdesk environments (configured here as an assistant for the Dezful Department of Education).

## Key Architectural Features
* **Local LLM Isolation:** Built to interact purely with local inference engines via the Ollama API, ensuring data privacy and removing reliance on cloud APIs.

* **Optimized Persian Processing:** Configured out-of-the-box to leverage `partai/dorna-llama3:8b`, a specialized model fine-tuned for high-accuracy Persian syntax and Right-to-Left (RTL) token context.

* **Real-time Engine Streaming:** Utilizes Python generators to pull chunks from the LLM stream asynchronously, ensuring zero UI freeze and low-latency interaction.

* **Structured Metadata Reporting:** Uses Pandas to poll the local machine's model registry, dynamically calculating and mapping sizes (Bytes to GBs), quantization tags, and model families into a clean startup summary.
---

## Repository Structure
```plaintext
ollama-local-agent-cli/
├── LICENSE          # Project licensing
├── README.md        # Documentation and setup instructions
├── main.py          # Core application script (Registry check & chat engine)
└── requirements.txt # External Python package dependencies
```
---

## Prerequisites & Setup
1. **Install Ollama**
Ensure you have Ollama installed locally on your machine. If you don't have it yet, download it from ollama.com.

2. **Pull the Targeted Model**
Open your terminal and pull the Persian-optimized Llama3 model used in this project:

```bash
ollama pull partai/dorna-llama3:8b-instruct-q4_0
```
3. **Clone and Install Dependencies**
Clone this repository, navigate to the folder, and install the required libraries using the `requirements.txt` file:

```bash
git clone https://github.com/your-username/ollama-local-agent-cli.git
cd ollama-local-agent-cli
pip install -r requirements.txt
```
---

## Usage
Launch the interactive assistant directly from your terminal:

```bash
python main.py
```
### What happens under the hood:
1. **Registry Audit:** The script scans your local Ollama service, formats the active models into a clean table using Pandas, and prints it to the console.

2. **Context Injection:** It initializes a customized `system_prompt` outlining specific organizational rules, forbidden response loops, and structural business answers.

3. **Loop Activation:** It drops you into a continuous CLI chat loop. Type your prompts in Persian, watch the responses stream token-by-token, and type `خداحافظ` whenever you want to close the session safely.
---

## Technology Stack
* **Language:** Python 3.10+

* **Core Framework:** `ollama-python`

* **Data Processing:** `pandas`

* **LLM Architecture Supported:** Llama 3 (Fine-tuned for localized Persian workflows)
