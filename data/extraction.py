import pandas as pd
import os



# Chargement ciblé
file_path = "CIS_COMPO_bdpm.txt"
output_path = "./substances_essentielles.csv"

try:
    # On définit les colonnes de la source
    cols = ['CIS', 'Element', 'Code_Substance', 'Nom_Substance', 'Dosage', 'Ref_Dosage', 'Nature', 'Lien']
    
    # On lit le gros fichier
    df = pd.read_csv(file_path, sep='\t', names=cols, encoding='latin-1')
    
    # On ne garde que les substances actives (SA) et les colonnes clés
    # Cela réduit la taille du fichier de 80%
    df_minimal = df[df['Nature'] == 'SA'][['CIS', 'Nom_Substance']].drop_duplicates()
    
    # On sauvegarde la version "légère"
    df_minimal.to_csv(output_path, index=False)
    print(f"Extraction terminée : {output_path} créé.")

    # Suppression du gros fichier pour libérer de l'espace
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Fichier lourd {file_path} supprimé avec succès.")

except Exception as e:
    print(f"Erreur lors de l'optimisation : {e}")