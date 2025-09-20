# train_model.py
import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

print("🔧 Entraînement du modèle en cours...")

# 1. Charger les données nettoyées
df = pd.read_csv('cleaned_air_quality_20250919_2321.csv')
print(f"📊 Données chargées : {len(df)} lignes")

# 2. Encoder la ville
le = LabelEncoder()
df['city_encoded'] = le.fit_transform(df['city'])

# 3. Préparer les features et la target
features = ['city_encoded', 'hour', 'day_of_week', 'month']
target = 'aqi'

X = df[features]
y = df[target]

# 4. Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"📋 Division train/test : {len(X_train)} train, {len(X_test)} test")

# 5. Entraîner le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("✅ Modèle entraîné !")

# 6. Évaluer le modèle
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n📈 PERFORMANCE DU MODÈLE :")
print(f"MAE (Erreur Moyenne Absolue) : {mae:.2f} points AQI")
print(f"R² (Score de précision) : {r2:.3f}")

if r2 > 0.7:
    print("🎯 Excellent modèle !")
elif r2 > 0.5:
    print("👍 Modèle acceptable")
else:
    print("⚠️  Modèle à améliorer")

# 7. SAUVEGARDER le modèle et les encodeurs
joblib.dump(model, 'air_quality_model.pkl')
joblib.dump(le, 'label_encoder.pkl')
joblib.dump(features, 'model_features.pkl')

print("\n💾 Fichiers sauvegardés :")
print("   - air_quality_model.pkl (modèle entraîné)")
print("   - label_encoder.pkl (encodeur des villes)")
print("   - model_features.pkl (liste des features)")

# 8. Exemple de prédiction
print("\n🔮 Exemple de prédiction :")
sample_data = pd.DataFrame([[0, 14, 2, 9]], columns=features)  # Paris, 14h, Mercredi, Septembre
sample_pred = model.predict(sample_data)[0]
print(f"   Paris, 14h, Mercredi → AQI prédit : {sample_pred:.1f}")