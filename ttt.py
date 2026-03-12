from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "./chroma_db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

# 1. Récupérer toutes les métadonnées
data = db.get()
metadatas = data['metadatas']

if not metadatas:
    print("La base est vide !")
else:
    # 2. Voir les clés disponibles (ex: 'molecule', 'Section', 'source')
    print(f"Clés trouvées dans les métadonnées : {metadatas[0].keys()}")
    
    # 3. Voir les valeurs uniques pour la clé 'molecule'
    # Change 'molecule' par 'source' si c'est le nom que tu as utilisé en semaine 1
    mols = set([m.get('molecule') for m in metadatas])
    print(f"Valeurs 'molecule' présentes en base : {mols}")