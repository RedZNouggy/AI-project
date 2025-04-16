#!/usr/bin/env python3

import openai
from PyPDF2 import PdfReader
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    EMBEDDING_DEPLOYMENT_NAME,
    GPT_DEPLOYMENT_NAME,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_KEY,
    AZURE_SEARCH_INDEX_NAME
)
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

openai.api_type = "azure"
openai.base_url = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_version = AZURE_OPENAI_API_VERSION

def extract_text_from_pdf(pdf_path: str) -> str:
    '''
    Extracts and concatenates text content from all pages of a PDF file.

    Parameters:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: A single string containing the extracted text from all pages, separated by newlines.
              Pages without extractable text are skipped.
    '''
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def chunk_text(text, max_tokens=500):
    '''
    Splits a large text into smaller chunks based on sentence boundaries and a token limit.

    Parameters:
        text (str): The full input text to be chunked.
        max_tokens (int): Approximate maximum number of words (tokens) per chunk. Defaults to 500.

    Returns:
        list: A list of text chunks, each under the specified token limit.
    '''
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
    '''
    Generates an embedding vector for the given text using the specified OpenAI embedding model.

    Parameters:
        text (str): The input text to be embedded. Newlines are replaced with spaces.

    Returns:
        list: A list of floats representing the embedding vector.
    '''
    response = openai.embeddings.create(
        input=text.replace("\n", " "),
        model=EMBEDDING_DEPLOYMENT_NAME
    )
    return response['data'][0]['embedding']

def search_similar_chunks(query, k=3):
    '''
    Searches for the top-k most similar text chunks in the Azure Cognitive Search index based on vector similarity.

    Parameters:
        query (str): The query text used to generate the embedding for similarity search.
        k (int): The number of most similar chunks to retrieve. Defaults to 3.

    Returns:
        list: A list of strings representing the most relevant content chunks from the index.
    '''
    embedding = get_embedding(query)
    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )
    results = client.search(
        search_text=None,
        vector=VectorizedQuery(vector=embedding, k_nearest_neighbors=k, fields="embedding"),
        select=["content"]
    )
    return [doc["content"] for doc in results]

def ask_gpt(context, question):
    '''
    Sends a prompt to the GPT model with context and a user question, and returns the generated response.

    Parameters:
        context (str): Background or supporting information to guide the GPT's answer.
        question (str): The actual user query.
    
    Returns:
        str: The GPT-generated response based on the provided context and question.
    '''
    messages = [
        {"role": "system", "content": "Tu es un assistant utile."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    response = openai.completions.create(
        engine=GPT_DEPLOYMENT_NAME,
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
