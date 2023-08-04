from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import traceback
from utilities.LLMHelper import LLMHelper
import logging
from utilities.StreamlitHelper import StreamlitHelper

def generate_embeddings(text):
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    embeddings = response['data'][0]['embedding']
    return embeddings

try:
    StreamlitHelper.hide_footer()

    st.title("Costruzioni - Copilot Prezziari")
    
    llm_helper = LLMHelper()

    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.image(os.path.join('images','teamsystem-logo.jpeg'))
    
    import os  
    import json  
    import openai  
    from dotenv import load_dotenv  
    from tenacity import retry, wait_random_exponential, stop_after_attempt  
    from azure.core.credentials import AzureKeyCredential  
    from azure.search.documents import SearchClient  
  
    # Configure environment variables  
    service_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
    index_name = os.getenv('AZURE_SEARCH_INDEX_NAME')
    key = os.getenv('AZURE_SEARCH_KEY')

    openai.api_type = "azure"
    openai.api_key = os.getenv('OPENAI_API_KEY')
    openai.api_base = os.getenv('OPENAI_API_BASE') 
    openai.api_version = "2023-05-15"

    credential = AzureKeyCredential(key)

    # Pure Vector Search
    
    query = st.text_input(label="Query:")
    
    if st.button(label="Ricerca"):  
        search_client = SearchClient(service_endpoint, index_name, credential=credential)  
        results = search_client.search(
            search_text=None,  
            vector=generate_embeddings(query),
            top_k=5,
            vector_fields="contentVector",
            select=["title", "content", "category"],
        )  

        for result in results:
            st.info(f"Score: {result['@search.score']}")  
            st.success(f"{result['content']}")
    
except Exception:
    st.error(traceback.format_exc())