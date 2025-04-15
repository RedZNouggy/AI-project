# AI-project
Groupe 49
# 🧠 Azure RAG PDF Indexer & Assistant

Ce projet est un **PoC RAG (Retrieval-Augmented Generation)** qui permet à GPT-4 d'interagir avec un ou plusieurs documents PDF hébergés localement, vectorisés et stockés dans **Azure AI Search**. L'utilisateur pose une question via une interface web (Streamlit), et GPT génère une réponse basée uniquement sur le contenu documentaire indexé.

---

[README in English](https://github.com/RedZNouggy/AI-project/blob/main/README-EN.MD)

## 📦 Fonctionnalités

- 🔍 Extraction automatique de texte depuis un ou plusieurs fichiers PDF
- ✂️ Découpage intelligent des documents en blocs sémantiques
- 🔢 Génération d'embeddings via `text-embedding-ada-002` (Azure OpenAI)
- 📥 Indexation des chunks vectorisés dans Azure AI Search
- 💬 Appel à GPT-4 avec contexte documentaire injecté
- 🌐 Interface utilisateur simple via Streamlit

---

## 📁 Structure du projet

```
.
├── config.py              # Paramètres Azure (clés, endpoints, noms de déploiements)
├── utils.py               # Fonctions utilitaires : extraction PDF, embeddings, chunking
├── index_data.py          # Script d'injection des documents PDF dans Azure Search
├── main.py                # Application frontend Streamlit (Q&A)
├── data/docs/             # Dossier contenant les PDF à indexer
└── requirements.txt       # Dépendances Python
```

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/RedZNouggy/AI-project.git
cd AI-project
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Remplir le fichier `config.py` avec les valeurs suivantes :

```python
AZURE_OPENAI_API_KEY = "<MY_API_KEY>"
AZURE_OPENAI_ENDPOINT = "https://<MY_URL>.openai.azure.com/"
AZURE_OPENAI_API_VERSION = "2023-05-15"

EMBEDDING_DEPLOYMENT_NAME = "text-embedding-ada-002"
GPT_DEPLOYMENT_NAME = "<GPT_DEPLOYMENT_NAME>"

AZURE_SEARCH_ENDPOINT = "https://<SEARCH_URL>.search.windows.net"
AZURE_SEARCH_KEY = "<SEARCH_API_KEY>"
AZURE_SEARCH_INDEX_NAME = "rag-index"
```

---

## 📄 Injection des documents PDF

Dépose tes fichiers PDF dans le dossier `data/docs/` :

```
data/docs/
├── contrat_client.pdf
├── norme_iso27001.pdf
└── politique_sécurité.pdf
```

Puis lance :

```bash
python index_data.py
```

✔️ Ce script :
- Crée (ou met à jour) l’index `rag-index`
- Injecte tous les documents PDF du dossier `data/docs/`
- Ajoute un champ `source` pour identifier d’où viennent les chunks

---

## 💬 Lancer l’interface utilisateur

```bash
streamlit run main.py
```

L’interface web s’ouvre automatiquement à [http://localhost:8501](http://localhost:8501)

---

## 🧠 Exemple d’utilisation

> 💬 **Question** : Combien de temps faut-il faire cuire un fondant au chocolat ?
> 🤖 **Réponse** : Selon la recette (source : livre_recettes_chocolat.pdf), le fondant au chocolat doit cuire 10 à 12 minutes à 180°C pour obtenir un cœur coulant.
> 💬 **Question :** Quels sont les délais de résolution en cas de panne critique ?  
> 🤖 **Réponse :** Selon le contrat (source : contrat_client.pdf), les pannes critiques doivent être traitées sous 4h ouvrées.

---

## 🛡️ Sécurité

- Aucun contenu n’est envoyé à des tiers hors Azure.
- Les documents PDF restent locaux, seuls les vecteurs sont stockés dans Azure Search.
- GPT n'a accès qu’au contexte injecté.

---

## 📌 Prérequis Azure

- Azure OpenAI avec :
  - Déploiement `gpt-4`
  - Déploiement `text-embedding-ada-002`
- Azure AI Search (`Basic` ou supérieur)

---

## 📃 Licence

Projet démonstratif
