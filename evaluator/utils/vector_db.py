import chromadb
import os
from django.conf import settings

def get_chroma_client():
    """
    Returns a persistent ChromaDB client.
    """
    db_path = os.path.join(settings.BASE_DIR, 'chroma_db')
    return chromadb.PersistentClient(path=db_path)

def store_cv_embedding(cv_id, text, metadata):
    """
    Stores the CV text in ChromaDB.
    """
    client = get_chroma_client()
    print("DEBUG: Loading ChromaDB collection (this may download the model on first run)...")
    collection = client.get_or_create_collection(name="cv_embeddings")
    
    # We use the CV ID as the document ID
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[str(cv_id)]
    )

def query_cvs(query_text, n_results=5):
    """
    Queries the CV embeddings.
    """
    client = get_chroma_client()
    collection = client.get_or_create_collection(name="cv_embeddings")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results
