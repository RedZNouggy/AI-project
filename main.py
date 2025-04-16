#!/usr/bin/env python3

import streamlit as st
from utils import search_similar_chunks, ask_gpt

st.title("IA - Groupe 49 (RAG)")
query = st.text_input("ask your questions about cooking...")

if query:
    st.write("Searching for context...")
    context_chunks = search_similar_chunks(query)
    context = "\n\n".join(context_chunks)
    
    st.write("Generating answer...")
    answer = ask_gpt(context, query)
    
    st.markdown("### Answer :")
    st.write(answer)
