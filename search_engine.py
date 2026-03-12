import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

#  Configuration des chemins
CHROMA_PATH = "./chroma_db"
CSV_PATH = "./data/mapping_expert_final.csv"


def get_molecule_from_brand(brand_name):
    """Cherche la molécule via le nom commercial (colonne 'nom')."""
    df = pd.read_csv(CSV_PATH)
    
    # On cherche si 'brand_name' (ex: Doliprane) est contenu dans la colonne 'nom'
    # na=False évite les erreurs si des cases sont vides
    mask = df['Nom'].str.contains(brand_name, case=False, na=False)
    result = df[mask]
    
    if not result.empty:
        # On renvoie la substance associée (colonne 'nom_substance')
        return result.iloc[0]['Nom_Substance'].replace('É','E')
    return None


def search_with_filter(brand_query, pathology_query , k=2):
    """Effectue une recherche RAG limitée à la molécule concernée."""
    
    # Étape A : Identification de la molécule
    molecule = get_molecule_from_brand(brand_query)
    if not molecule:
        return f"Désolé, le médicament '{brand_query}' n'est pas dans notre base."

    # Étape B : Initialisation du moteur (Embeddings + DB)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Étape C : Recherche filtrée
    # On utilise l'argument 'where' pour forcer Chroma à ne regarder que cette molécule
    results = db.similarity_search(
        pathology_query, 
        k=k, 
        filter={"molecule": molecule}
    )

    return results, molecule




def generate_answer(docs, question, molecule):
    # 1. On prépare le contexte avec les extraits trouvés
    context = "\n\n".join([f"[Section {d.metadata.get('Section')}]: {d.page_content}" for d in docs])
    
    # 2. Le "Prompt" : on donne des instructions strictes à l'IA
    template = f"""
    Tu es un assistant pharmacien expert en {molecule}.
    Utilise UNIQUEMENT les extraits de la notice officielle ci-dessous pour répondre à la question du patient.
    
    RÈGLES :
    1. Si la réponse n'est pas dans le texte, dis explicitement que la notice ne le précise pas.
    2. Cite toujours le numéro de la section.
    3. Sois très prudent et rigoureux (contexte médical).

    NOTICE OFFICIELLE :
    {context}

    QUESTION : {question}
    RÉPONSE :"""

    # 3. Appel du modèle (ex: Mistral ou Gemma)
    # Note : Il faut avoir lancé 'ollama run mistral' au préalable
    
    #llm = Ollama(model="mistral")
    llm = Ollama(model="qwen2.5:0.5b")
    return llm.invoke(template)




 # --- TEST DU SCRIPT ---
if __name__ == "__main__":
    medicament = "Doliprane"
    question = "problème de foie sévère"

    print(f"--- Analyse pour : {medicament} ---")
    docs, mol_name = search_with_filter(medicament, question)
    
    if docs is None:
        print(f"Erreur : {mol_name}")
    else:
        print(f"Molécule identifiée : {mol_name}")
        for i, doc in enumerate(docs):
            print(f"\n[Source : Section {doc.metadata['Section']}]")
            print(f"Extrait : {doc.page_content[:200]}...")