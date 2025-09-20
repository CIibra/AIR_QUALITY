# 🌍 AirQuest - Application de Prédiction de la Qualité de l'Air 

**Une application end-to-end de Data Science** qui collecte, prédit et visualise la qualité de l'air en France en temps réel.

## 🚀 Fonctionnalités

- **📡 Collecte de données temps réel** via des APIs (OpenWeather, WAQI)
- **🤖 Modèle de Machine Learning** (Random Forest) pour prédire l'AQI
- **📊 Dashboard interactif** avec visualisations (Heatmaps, Timeseries)
- **🌐 Application Web** déployée et accessible à tous

## 🛠️ Stack Technique

| Domaine | Technologies |
|---------|-------------|
| **Data Collection** | Python, Requests, APIs REST |
| **Data Cleaning** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, Joblib |
| **Data Visualization** | Matplotlib, Seaborn, Plotly |
| **Web App** | Streamlit |
| **Deployment** | Streamlit Cloud, GitHub Actions |

## 📈 Résultats du Modèle

- **MAE (Mean Absolute Error)**: 4.73 points AQI
- **R² Score**: 0.546
- **Temps d'entraînement**: < 4 minutes

## 🖥️ Comment Lancer l'Application Localement

```bash
git clone https://github.com/votrepseudo/AirQuest-AQI-Prediction-App.git
cd AirQuest-AQI-Prediction-App
pip install -r requirements.txt
streamlit run src/pratical_app.py
```

## 🔮 Améliorations Futures 
- [ ] Intégrer des données satellites
- [ ] Notifications alertes pollution
