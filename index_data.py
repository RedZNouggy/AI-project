#!/usr/bin/env python3

import os
import uuid
from messages import (
    infotext,
    successtext
)
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, VectorSearch, HnswAlgorithmConfiguration
)
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_KEY,
    AZURE_SEARCH_INDEX_NAME
)
from utils import extract_text_from_pdf, chunk_text, get_embedding

def create_index():
    '''
    Creates or updates an Azure Cognitive Search index with fields suitable for semantic search.

    The index includes:
        - A unique string ID (`id`)
        - Searchable text content (`content`)
        - A source identifier (`source`)
        - A vector embedding field (`embedding`) configured for HNSW-based vector search

    Uses the `AZURE_SEARCH_KEY`, `AZURE_SEARCH_ENDPOINT`, and `AZURE_SEARCH_INDEX_NAME` 
    environment/configuration variables.

    Returns:
        None
    '''
    credential = AzureKeyCredential(AZURE_SEARCH_KEY)
    index_client = SearchIndexClient(endpoint=AZURE_SEARCH_ENDPOINT, credential=credential)

    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="content", type="Edm.String"),
        SearchableField(name="source", type="Edm.String"),
        SearchableField(name="embedding", dimensions=1536, vector_search_configuration="default")
    ]

    vector_search = VectorSearch(
        algorithm_configurations=[
            HnswAlgorithmConfiguration(name="default")
        ]
    )

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX_NAME,
        fields=fields,
        vector_search=vector_search
    )
    infotext(f"Trying to create the index {AZURE_SEARCH_INDEX_NAME}...")
    index_client.create_or_update_index(index)
    successtext(f"The Index : {AZURE_SEARCH_INDEX_NAME} has been successfully created.")

def upload_chunks(pdf_path, source):
    '''
    Extracts text from a PDF, splits it into chunks, generates embeddings, and uploads
    the resulting documents to an Azure Cognitive Search index.

    Parameters:
        pdf_path (str): The path to the PDF file to be processed.
        source (str): A label or identifier representing the source of the document (e.g., filename or context).

    Returns:
        None
    '''
    credential = AzureKeyCredential(AZURE_SEARCH_KEY)
    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=credential
    )
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    docs = []
    for chunk in chunks:
        docs.append({
            "id": str(uuid.uuid4()),
            "content": chunk,
            "embedding": get_embedding(chunk),
            "source": source
        })
    search_client.upload_documents(docs)
    successtext(f"The data of the document : {pdf_path} has been successfully imported.")

if __name__ == "__main__":
    create_index()
    for filename in os.listdir("data/docs/"):
        if filename.endswith(".pdf"):
            infotext(f"Processing on the file {filename}...")
            upload_chunks(os.path.join("data/docs/", filename), source=filename)
