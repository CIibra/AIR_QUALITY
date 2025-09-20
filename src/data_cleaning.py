import pandas as pd
import numpy as np
from datetime import datetime
import glob

def load_and_clean_data():
    """Charge et nettoie tous les fichiers de données"""
    # 1. Charger tous les fichiers CSV
    all_files = glob.glob("air_quality_data_*.csv")
    if not all_files:
        print("Aucun fichier de données trouvé!")
        return None
    
    # 2. Fusionner tous les fichiers
    dfs = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"Chargé: {file} ({len(df)} lignes)")
        except Exception as e:
            print(f"Erreur avec {file}: {e}")
    
    if not dfs:
        return None
    
    # 3. Concaténer tous les DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Dataset combiné: {len(combined_df)} lignes")
    
    # 4. Nettoyage de base
    # Supprimer les doublons exacts
    initial_count = len(combined_df)
    combined_df = combined_df.drop_duplicates()
    print(f"Doublons supprimés: {initial_count - len(combined_df)}")
    
    # Convertir la colonne timestamp en datetime
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], errors='coerce')
    
    # Supprimer les lignes avec timestamp invalide
    combined_df = combined_df.dropna(subset=['timestamp'])
    
    # Trier par timestamp
    combined_df = combined_df.sort_values('timestamp')
    
    # 5. Gestion des valeurs manquantes
    print("\nValeurs manquantes avant traitement:")
    print(combined_df.isnull().sum())
    
    # Remplacer les valeurs manquantes dans dominant_pollutant
    combined_df['dominant_pollutant'] = combined_df['dominant_pollutant'].fillna('Inconnu')
    
    # Pour AQI, on pourrait interpoler ou supprimer, mais attention!
    # Ici on supprime les lignes sans AQI
    combined_df = combined_df.dropna(subset=['aqi'])
    
    # 6. Détection des valeurs aberrantes (outliers)
    # Exemple: AQI normalement entre 0 et 500
    Q1 = combined_df['aqi'].quantile(0.25)
    Q3 = combined_df['aqi'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = combined_df[(combined_df['aqi'] < lower_bound) | (combined_df['aqi'] > upper_bound)]
    print(f"\nValeurs aberrantes détectées: {len(outliers)}")
    
    # On garde les outliers pour l'analyse, mais on pourrait les filtrer elle peut révéler des evenements : pollution, 
    # mais tout pour le modèle elle peut lui faire apprendre mal...
    combined_df = combined_df[(combined_df['aqi'] >= lower_bound) & (combined_df['aqi'] <= upper_bound)]
    
    # 7. Ajouter des features temporelles
    combined_df['hour'] = combined_df['timestamp'].dt.hour
    combined_df['day_of_week'] = combined_df['timestamp'].dt.dayofweek
    combined_df['month'] = combined_df['timestamp'].dt.month
    combined_df['date'] = combined_df['timestamp'].dt.date
    
    # 8. Sauvegarder le dataset nettoyé
    cleaned_filename = f"cleaned_air_quality_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    combined_df.to_csv(cleaned_filename, index=False)
    
    print(f"\nNettoyage terminé! Dataset sauvegardé sous: {cleaned_filename}")
    print(f"Lignes finales: {len(combined_df)}")
    print(f"Période couverte: {combined_df['timestamp'].min()} to {combined_df['timestamp'].max()}")
    
    return combined_df

if __name__ == "__main__":
    df_clean = load_and_clean_data()
    if df_clean is not None:
        print("\nAperçu des données nettoyées:")
        print(df_clean.head())
        print("\nInfos basiques:")
        print(df_clean.info())