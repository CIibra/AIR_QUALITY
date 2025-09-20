import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Charger les données
df = pd.read_csv('cleaned_air_quality_20250919_2321.csv')

# 2. Convertir la colonne timestamp en datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 3. Extraire l'heure pour les analyses
df['hour'] = df['timestamp'].dt.hour

# 4. Vérifier la période couverte
print("Période des données :")
print(f"De : {df['timestamp'].min()}")
print(f"À : {df['timestamp'].max()}")
print(f"Nombre d'heures uniques : {df['hour'].nunique()}")

# 5. Distribution de l'AQI par ville (reste valable)
plt.figure(figsize=(12, 6))
sns.boxplot(x='city', y='aqi', data=df)
plt.title('Distribution de la qualité de l\'air par ville')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. ÉVOLUTION HORAIRE - Moyenne toutes villes confondues
plt.figure(figsize=(14, 6))
df.groupby('hour')['aqi'].mean().plot(marker='o', linestyle='-', linewidth=2)
plt.title('Évolution horaire de la qualité de l\'air (moyenne toutes villes)')
plt.xlabel('Heure de la journée')
plt.ylabel('AQI moyen')
plt.xticks(range(0, 24))  # Toutes les heures
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 7. ÉVOLUTION HORAIRE PAR VILLE - Beaucoup plus intéressant !
plt.figure(figsize=(14, 8))

for city in df['city'].unique():
    city_data = df[df['city'] == city]
    hourly_avg = city_data.groupby('hour')['aqi'].mean()
    plt.plot(hourly_avg.index, hourly_avg.values, 
             label=city, marker='o', markersize=6, linewidth=2)

plt.title('Évolution horaire de l\'AQI par ville')
plt.xlabel('Heure de la journée')
plt.ylabel('AQI moyen')
plt.xticks(range(0, 24))
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 8. Heatmap de l'AQI par heure et par ville (TRÈS visuel)
plt.figure(figsize=(12, 8))
pivot_data = df.pivot_table(values='aqi', index='hour', columns='city', aggfunc='mean')
sns.heatmap(pivot_data, annot=True, cmap='RdYlGn_r', fmt='.1f', 
            cbar_kws={'label': 'AQI moyen'})
plt.title('Heatmap de l\'AQI moyen par heure et par ville')
plt.xlabel('Ville')
plt.ylabel('Heure de la journée')
plt.tight_layout()
plt.show()

# 9. Analyse des polluants dominants par heure
plt.figure(figsize=(14, 6))
pollutant_by_hour = df.groupby('hour')['dominant_pollutant'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Inconnu')
pollutant_by_hour.value_counts().plot(kind='bar')
plt.title('Polluant dominant sur la journée')
plt.xlabel('Polluant')
plt.ylabel('Nombre d\'heures où il est dominant')
plt.tight_layout()
plt.show()