import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma



# On définit le chemin absolu pour éviter les erreurs de dossier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Connexion à la base existante
if not os.path.exists(CHROMA_PATH):
    print(f"Erreur : La base {CHROMA_PATH} n'existe pas. Lance d'abord chuncking.py")
else:
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Requête de test
    query = "Le patient a une maladie grave du foie"
    print(f"\n Test de recherche pour : '{query}'")
    
    # On demande les 2 meilleurs résultats
    results = db.similarity_search(query, k=2)

    for i, doc in enumerate(results):
        print(f"\n--- RÉSULTAT N°{i+1} ---")
        print(f"Molécule détectée : {doc.metadata.get('molecule')}")
        print(f"Section de la notice : {doc.metadata.get('Section')}")
        print(f"Contenu : {doc.page_content[:250]}...")