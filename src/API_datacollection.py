import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import json

# Configuration des APIs
OWM_API_KEY = "05c754d2e335f1843b9aa97dd970e634"
WAQI_TOKEN = "41143a917534da3a3c487e39b4183c6d4bf01879"
CITIES = ["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux"]

# Configuration de la collecte
COLLECTION_DURATION = timedelta(hours=3)  # Durée totale de collecte
INTERVAL_MINUTES = 20  # Intervalle entre les collectes en minutes
MAX_RECORDS = 1000  # Nombre maximum d'enregistrements à collecter

def get_air_quality(city):
    """Récupère les données de qualité de l'air pour une ville"""
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_TOKEN}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok':
            aqi = data['data']['aqi']
            dominentpol = data['data']['dominentpol']
            return {
                'city': city,
                'aqi': aqi,
                'dominant_pollutant': dominentpol,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        print(f"Erreur pour {city}: {e}")
    return None

def collect_data():
    """Fonction principale pour collecter les données"""
    all_data = []
    start_time = datetime.now()
    end_time = start_time + COLLECTION_DURATION
    
    print(f"Début de la collecte à {start_time}")
    print(f"La collecte durera {COLLECTION_DURATION} ou jusqu'à {MAX_RECORDS} enregistrements")
    
    while datetime.now() < end_time and len(all_data) < MAX_RECORDS:
        cycle_data = []
        
        for city in CITIES:
            aq_data = get_air_quality(city)
            if aq_data:
                cycle_data.append(aq_data)
                print(f"{datetime.now().strftime('%H:%M:%S')} - Données collectées pour {city}: AQI = {aq_data['aqi']}")
            
            # Pause courte entre les requêtes pour une même ville
            time.sleep(1)
        
        # Ajouter les données de ce cycle à l'ensemble
        all_data.extend(cycle_data)
        
        # Sauvegarder les données après chaque cycle
        if cycle_data:
            df = pd.DataFrame(cycle_data)
            filename = f"air_quality_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            df.to_csv(filename, index=False)
            print(f"Données sauvegardées dans {filename}")
        
        # Afficher le statut
        print(f"Progression: {len(all_data)}/{MAX_RECORDS} enregistrements - "
              f"Temps restant: {end_time - datetime.now()}")
        
        # Attendre jusqu'à la prochaine collecte
        if datetime.now() + timedelta(minutes=INTERVAL_MINUTES) < end_time and len(all_data) < MAX_RECORDS:
            print(f"Prochaine collecte dans {INTERVAL_MINUTES} minutes...")
            time.sleep(INTERVAL_MINUTES * 60)
    
    # Sauvegarder toutes les données dans un fichier final
    if all_data:
        final_df = pd.DataFrame(all_data)
        final_filename = f"air_quality_complete_{start_time.strftime('%Y%m%d_%H%M')}_to_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        final_df.to_csv(final_filename, index=False)
        print(f"Collecte terminée. {len(all_data)} enregistrements sauvegardés dans {final_filename}")
    
    return all_data

if __name__ == "__main__":
    data = collect_data()
    print(f"Collecte terminée. {len(data)} enregistrements collectés.")