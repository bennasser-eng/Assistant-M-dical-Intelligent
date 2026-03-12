import pandas as pd
import os

# Chargement du fichier CIS_bdpm
file_id = "CIS_bdpm.txt"
file_substances = "./substances_essentielles.csv"
output_final = "./mapping_expert_final.csv"


try:
    # On définit les colonnes pour CIS_bdpm
    cols_id = ['CIS', 'Nom', 'Forme', 'Voie', 'Statut', 'Proc', 'Etat', 'Date', 'Statut_B', 'CE', 'Titulaire', 'Surv']
    
    # On ne charge que CIS et Nom pour économiser la RAM
    df_id = pd.read_csv(file_id, sep='\t', names=cols_id, encoding='latin-1', usecols=['CIS', 'Nom', 'Etat'])
    
    # On filtre pour ne garder que les médicaments commercialisés
    df_id = df_id[df_id['Etat'] == 'Commercialisée'][['CIS', 'Nom']]

    # Chargement du fichier substances
    df_sub = pd.read_csv(file_substances)

    # La Fusion (Join) : on lie le Nom Commercial à la Substance via le code CIS
    df_final = pd.merge(df_id, df_sub, on='CIS')

    # Sauvegarde du fichier "Maître"
    df_final.to_csv(output_final, index=False, encoding='utf-8')
    
    print(f"Extraction réussie ! Fichier final créé : {output_final}")
    print(f"Nombre total de correspondances : {len(df_final)}")

    # Nettoyage du disque (Mémoire PC)
    if os.path.exists(file_id):
        os.remove(file_id)
        print(f"Fichier source {file_id} supprimé.")
    if os.path.exists(file_substances):
        os.remove(file_substances)
        print(f"Fichier temporaire {file_substances} supprimé.")

except Exception as e:
    print(f"Erreur lors de la fusion : {e}")