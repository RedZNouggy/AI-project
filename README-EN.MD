# AI-project

# 🧠 Azure RAG PDF Indexer & Assistant (EN)

This project is a **RAG (Retrieval-Augmented Generation) PoC** that enables GPT-4 to interact with one or more locally hosted PDF documents, vectorized and stored in **Azure AI Search**. The user asks a question via a web interface (Streamlit), and GPT generates an answer based solely on the indexed document content.

---

## 📦 Features

- 🔍 Automatic text extraction from one or more PDF files
- ✂️ Intelligent document segmentation into semantic chunks
- 🔢 Embedding generation via `text-embedding-ada-002` (Azure OpenAI)
- 📥 Indexing of vectorized chunks in Azure AI Search
- 💬 Call to GPT-4 with injected document context
- 🌐 Simple user interface via Streamlit

---

## 📁 Project Structure

```
.
├── config.py              # Paramètres Azure (clés, endpoints, noms de déploiements)
├── utils.py               # Fonctions utilitaires : extraction PDF, embeddings, chunking
├── index_data.py          # Script d'injection des documents PDF dans Azure Search
├── main.py                # Application frontend Streamlit (Q&A)
├── messages.py            # Info, sucess, error, warning colored messages
├── data/docs/             # Dossier contenant les PDF à indexer
└── requirements.txt       # Dépendances Python
```

---

## ⚙️ Installation

### 1. Clone the project

```bash
git clone https://github.com/RedZNouggy/AI-project.git
cd AI-project
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Fill the `config.py` file with the following values:

```python
AZURE_OPENAI_API_KEY = "<MY_API_KEY>"
AZURE_OPENAI_ENDPOINT = "https://<MY_URL>.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"

EMBEDDING_DEPLOYMENT_NAME = "text-embedding-ada-002"
GPT_DEPLOYMENT_NAME = "<GPT_DEPLOYMENT_NAME>"

AZURE_SEARCH_ENDPOINT = "https://<SEARCH_URL>.search.windows.net"
AZURE_SEARCH_KEY = "<SEARCH_API_KEY>"
AZURE_SEARCH_INDEX_NAME = "rag-index"
```

---

## 📄 PDF Document Injection

Drop your PDF files into the folder `data/docs/` :

```
data/docs/
├── contrat_client.pdf
├── norme_iso27001.pdf
└── politique_sécurité.pdf
```

Then run :

```bash
python index_data.py
```

✔️ This script:
- Creates (or updates) the `rag-index` index
- Injects all PDF documents from the `data/docs/` folder
- Adds a `source` field to identify where the chunks come from

---

## 💬 Launch the User Interface

```bash
streamlit run main.py
```

The web interface will automatically open at [http://localhost:8501](http://localhost:8501)

---

## 🧠 Usage Example

> 💬 **Question**: How long should a chocolate fondant be baked for?
> 🤖 **Answer**: According to the recipe (source: livre_recettes_chocolat.pdf), the chocolate fondant should be baked for 10 to 12 minutes at 180°C to obtain a runny center.
> 💬 **Question:** What are the resolution times in the event of a critical failure?
> 🤖 **Answer:** According to the contract (source: contrat_client.pdf), critical failures must be processed within 4 business hours.

---

## 🛡️ Security

- No content is sent to third parties outside Azure.
- PDF documents remain local; only the vectors are stored in Azure Search.
- GPT only has access to the injected context.

---

## 📌 Azure Requirements

- Azure OpenAI with :
  - Déploiement `gpt-4`
  - Déploiement `text-embedding-ada-002`
- Azure AI Search (`Basic` or more)

---

## 📃 License

Demonstration project
