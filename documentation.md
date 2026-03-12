# RAG (Retrieval-Augmented Generation) et Agents AI.

## Choix du Domaine : "Interactions Médicamenteuses et Contre-indications"
* Données Structurées : Les sources (Vidal, ANSM, bases publiques) sont très factuelles.

* Criticités : C'est un excellent test pour un Agent IA. Une erreur ici est binaire (vrai/faux), ce qui facilite l'évaluation technique.

* Valeur Pro : Créer un outil capable de croiser une prescription avec une pathologie patient est un cas d'usage complexe et recherché.

###### Workflow de l'Agent RAG

* Analyse : Reformulation de la requête (Query Transformation).

* Routage : L'agent détermine si la réponse est dans la base vectorielle ou nécessite une recherche web.

* Récupération : Recherche hybride (Vectorielle + BM25).

* Reranking : Utilisation d'un modèle de Rerank pour prioriser les chunks les plus précis.

* Génération & Critique : Vérification des hallucinations (Faithfulness).
    
    
##### L'Objectif de l'Agent (Le "MVP")

Développer un Agent RAG capable de vérifier si un nouveau médicament prescrit présente un risque pour un patient donné, en se basant exclusivement sur des notices médicales officielles.
Fonctionnalités cibles :

* Extraction : Identifier les molécules dans une question.

* Retrieval : Chercher uniquement dans une base de données de notices PDF/JSON locale (pas de recherche web sauvage).

* Raisonnement : "Le patient prend X et a une pathologie Y. Le médicament Z est-il sûr ?"

 * Justification : L'agent doit citer la section précise du document source (ex: "Section 4.3 : Contre-indications").
 
 
 
## Etape1: Setup 1 Ingestion 
 
 medical_rag/
├── data/               # Rangez vos PDF ici
├── vector_db/          # Sera créé automatiquement par ChromaDB
├── main.py             # Votre script d'ingestion
└── notes_recherche.md  # Votre fichier Markdown de suivi
 
* Instalation  de **ollama** 

 
 
#### Telechargement de CIS_bdpm.txt  CIS_COMPO_bdpm.txt depuis le site 
https://base-donnees-publique.medicaments.gouv.fr/telechargement

* application de code extraction sur le fichier CIS_COMPO_bdpm.txt  pour avoir en fin CIS_COMPO_bdpm.csv
* application de code fusion sur le fichier  CIS_bdpm.txt pour avoir en fin  CIS_bdpm.csv , et en fin les fusioner les deux 
pour avoir un seul fichier qui rensemble tous les infos : **mapping_expert_final.csv**



#### telechargment des notices pour des substances populaires comme paracetamol 
via le lien 
**base-donnees-publique.medicaments.gouv.fr "4.3. Contre-indications" amoxicilline.**






## Etape2: Embedding des fichiers de notices/

* **Le "Chunking" Stratégique (Le découpage)**

Un LLM a une fenêtre de contexte limitée et le bruit nuit à la précision. Si on lui envoie toute la notice, il risque de se perdre. On découpe donc le document en "Chunks".

le découpage par caractères (chunk_size=1000) est souvent médiocre car il coupe au milieu d'une phrase. Nous utilisons le **MarkdownHeaderTextSplitter** : il utilise tes balises ## comme frontières naturelles.

Pourquoi c'est supérieur ?
Chaque morceau de texte extrait saura s'il appartient à la section "Contre-indications" ou "Interactions", car ce titre sera injecté dans les métadonnées du vecteur.


### L'architecture de LangChain est désormais modulaire :

* **langchain-core** : Les interfaces de base.

* **langchain-huggingface** : Les modèles d'embeddings (déjà installé).

* **langchain-text-splitters** : Les algorithmes de découpage de texte (ce qu'il te manque).

* **langchain-community** : Les intégrations comme ChromaDB.




































