import sys
print(sys.executable)
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter

# --- ÉTAPE A : Configuration du moteur mathématique ---
# Ce modèle est chargé une seule fois en RAM
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
encode_kwargs = {'normalize_embeddings': True}    # Pour utiliser la similarité cosinus simple


embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)




# --- ÉTAPE B : Parsing des notices ---
headers_to_split_on = [("##", "Section")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

documents_a_indexer = []
notices_path = "."

for file in os.listdir(notices_path):
    if file.endswith(".md"):
        with open(os.path.join(notices_path, file), 'r', encoding='utf-8') as f:
            raw_text = f.read()
            # Découpage sémantique
            chunks = markdown_splitter.split_text(raw_text)
            
            # On enrichit chaque chunk avec le nom de la molécule (clé de filtrage)
            molecule_name = file.replace(".md", "").upper()
            for chunk in chunks:
                chunk.metadata["molecule"] = molecule_name
            
            documents_a_indexer.extend(chunks)

            
            
# --- ÉTAPE C : Stockage Vectoriel ---
# ChromaDB va créer un dossier ./chroma_db sur le disque
vector_db = Chroma.from_documents(
    documents=documents_a_indexer,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
vector_db.persist()
print(f"Phase 2 terminée. {len(documents_a_indexer)} vecteurs créés pour {notices_path}")