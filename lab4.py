import streamlit as st
import openai
from PyPDF2 import PdfReader

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb

# Define your function to create the ChromaDB collection
def create_lab4_chromadb():
    if 'Lab4_vectorDB' not in st.session_state:
        # Initialize ChromaDB client
        client = chromadb.Client()
        
        # Create a collection
        collection = client.create_collection("Lab4Collection")

        # Load PDF files and convert to text
        pdf_files = ["file1.pdf", "file2.pdf", "file3.pdf", "file4.pdf", "file5.pdf", "file6.pdf", "file7.pdf"]  # Replace with actual file paths
        texts = []
        for file in pdf_files:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            texts.append({"text": text, "metadata": {"filename": file}})

        # Embed the text using OpenAI
        embeddings = []
        for doc in texts:
            response = openai.Embedding.create(input=doc['text'], model="text-embedding-ada-002")  # Replace with the correct model
            embedding = response['data'][0]['embedding']
            embeddings.append(embedding)

        # Add data to ChromaDB collection
        for i, doc in enumerate(texts):
            collection.add(
                ids=[f"doc_{i}"],
                embeddings=[embeddings[i]],
                metadatas=[doc['metadata']]
            )
        
        # Save the collection to session state
        st.session_state.Lab4_vectorDB = collection

# Query ChromaDB collection
def query_lab4_chromadb(query_text):
    collection = st.session_state.Lab4_vectorDB
    response = collection.query(query_texts=[query_text], n_results=3)
    return response

# Add a Streamlit page for the Lab4 collection
st.title("Lab 4: ChromaDB with OpenAI Embeddings")
if st.button("Create ChromaDB Collection"):
    create_lab4_chromadb()
    st.write("ChromaDB Collection Created!")

query = st.text_input("Enter a query (e.g., 'Generative AI')")
if query and 'Lab4_vectorDB' in st.session_state:
    results = query_lab4_chromadb(query)
    st.write(f"Top 3 Results for query '{query}':")
    for result in results['documents']:
        st.write(result)
