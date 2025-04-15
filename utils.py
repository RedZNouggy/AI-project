import openai
from PyPDF2 import PdfReader
from config import *
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
from azure.core.credentials import AzureKeyCredential

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_version = AZURE_OPENAI_API_VERSION

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def chunk_text(text, max_tokens=500):
    sentences = text.split('.')
    chunks, current = [], ""
    for sentence in sentences:
        if len(current.split()) + len(sentence.split()) < max_tokens:
            current += sentence + '.'
        else:
            chunks.append(current.strip())
            current = sentence + '.'
    if current:
        chunks.append(current.strip())
    return chunks

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        engine=EMBEDDING_DEPLOYMENT_NAME
    )
    return response['data'][0]['embedding']

def search_similar_chunks(query, k=3):
    embedding = get_embedding(query)
    client = SearchClient(endpoint=AZURE_SEARCH_ENDPOINT,
                          index_name=AZURE_SEARCH_INDEX_NAME,
                          credential=AzureKeyCredential(AZURE_SEARCH_KEY))
    
    results = client.search(
        search_text=None,
        vector=Vector(value=embedding, k=k, fields="embedding"),
        select=["content"]
    )
    return [doc["content"] for doc in results]

def ask_gpt(context, question):
    messages = [
        {"role": "system", "content": "Tu es un assistant pour la cuisine"},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    response = openai.ChatCompletion.create(
        engine=GPT_DEPLOYMENT_NAME,
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
