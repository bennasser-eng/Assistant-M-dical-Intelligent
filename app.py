import streamlit as st
from search_engine import search_with_filter
from langchain_community.llms import Ollama

# --- CONFIGURATION DU GÉNÉRATEUR ---
def generate_answer(docs, question, molecule):
    """Génère une réponse synthétique à partir des documents trouvés."""
    # Préparation du contexte
    context = "\n\n".join([f"[Section {d.metadata.get('Section', 'N/A')}]: {d.page_content}" for d in docs])
    
    # Prompt rigoureux
    template = f"""Tu es un assistant pharmacien expert en {molecule}.
Utilise UNIQUEMENT les extraits de la notice officielle ci-dessous pour répondre au patient.

RÈGLES :
1. Si l'information n'est pas dans le texte, dis que la notice ne le précise pas.
2. Cite les numéros de sections utilisées.
3. Sois concis et médicalement rigoureux.

NOTICE :
{context}

QUESTION : {question}
RÉPONSE :"""

    #llm = Ollama(model="mistral") # Assure-toi d'avoir installé 'mistral' avec Ollama
    llm = Ollama(model="qwen2.5:0.5b")

    return llm.invoke(template)

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Assistant Médical RAG", page_icon="💊")
st.title("Assistant Médical Intelligent")
st.markdown("Recherche sécurisée et synthèse par IA.")

# --- BARRE LATÉRALE ---
st.sidebar.header("Paramètres")
k_results = st.sidebar.slider("Nombre d'extraits à récupérer", 1, 5, 2)

# --- ZONE DE SAISIE ---
col1, col2 = st.columns(2)
with col1:
    medicament = st.text_input("Nom du médicament (ex: Doliprane)", "")
with col2:
    question = st.text_input("Votre question (ex: Foie, Grossesse...)", "")

# --- LOGIQUE PRINCIPALE ---
if st.button("Analyser la notice"):
    if medicament and question:
        with st.spinner("Analyse et génération en cours..."):
            # 1. Recherche (Retrieval)
            docs, mol_name = search_with_filter(medicament, question , k=k_results)
            
            if docs is None:
                st.error(f" {mol_name}")
            elif not docs:
                st.warning(f" Molécule '{mol_name}' identifiée, mais aucun extrait trouvé.")
            else:
                st.success(f" Molécule identifiée : **{mol_name.upper()}**")
                
                # 2. Génération (Generation)
                reponse_ia = generate_answer(docs, question, mol_name)
                
                st.subheader("🤖 Réponse de l'Assistant")
                st.info(reponse_ia)
                
                # 3. Affichage des sources (Transparency)
                st.divider()
                st.subheader("📄 Extraits sources utilisés")
                for i, doc in enumerate(docs):
                    with st.expander(f"Extrait {i+1} - Section {doc.metadata.get('Section', 'N/A')}"):
                        st.write(doc.page_content)
                        st.caption(f"Fichier : {mol_name}.md")
    else:
        st.warning("Veuillez remplir les deux champs.")