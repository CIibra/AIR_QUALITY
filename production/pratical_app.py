# app.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(page_title="AirQuest - Prédiction AQI", page_icon="🌍")

# 1. Chargement du modèle et des encodeurs
@st.cache_resource
def load_model():
    try:
        model = joblib.load('production/air_quality_model.pkl')
        le = joblib.load('production/label_encoder.pkl')
        features = joblib.load('production/model_features.pkl')
        return model, le, features
    except FileNotFoundError:
        st.error("❌ Fichiers modèle non trouvés. Exécutez d'abord 'predict_model.py'")
        st.stop()

model, le, features = load_model()

# 2. Interface utilisateur
st.title("🌍 AirQuest - Prédiction de la Qualité de l'Air")
st.markdown("Prédisez l'indice AQI en fonction de la ville et de l'heure")

# 3. Paramètres de prédiction
col1, col2 = st.columns(2)

with col1:
    ville = st.selectbox("🏙️ Ville", options=le.classes_.tolist())
    heure = st.slider("🕒 Heure de la journée", 0, 23, 12)

with col2:
    jour_semaine = st.selectbox("📅 Jour de la semaine", 
                               options=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
    mois = st.slider("📆 Mois", 1, 12, 9)

# 4. Conversion des valeurs
jour_map = {"Lundi": 0, "Mardi": 1, "Mercredi": 2, "Jeudi": 3, 
            "Vendredi": 4, "Samedi": 5, "Dimanche": 6}
jour_encoded = jour_map[jour_semaine]
ville_encoded = le.transform([ville])[0]

# 5. Création des features pour la prédiction
input_data = pd.DataFrame([[ville_encoded, heure, jour_encoded, mois]], 
                         columns=features)

# 6. Prédiction
if st.button("🚀 Prédire l'AQI", type="primary"):
    with st.spinner("Calcul en cours..."):
        prediction = model.predict(input_data)[0]
    
    # Affichage des résultats
    st.success("Prédiction terminée !")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="**AQI Prédit**", value=f"{prediction:.1f}")
    
    with col2:
        if prediction < 50:
            st.metric(label="**Qualité**", value="✅ Bonne")
        elif prediction < 100:
            st.metric(label="**Qualité**", value="⚠️ Moyenne")
        else:
            st.metric(label="**Qualité**", value="❌ Mauvaise")
    
    with col3:
        st.metric(label="**Précision**", value="±4 points")
    
    # Détails techniques
    with st.expander("📋 Détails techniques"):
        st.write("**Paramètres utilisés :**")
        st.write(f"- Ville : {ville} (code: {ville_encoded})")
        st.write(f"- Heure : {heure}h")
        st.write(f"- Jour : {jour_semaine} (code: {jour_encoded})")
        st.write(f"- Mois : {mois}")
        st.write(f"- Features : {features}")

# 7. Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    Cette application prédit l'**Indice de Qualité de l'Air (AQI)** 
    en utilisant un modèle de Machine Learning.
    
    **Échelle AQI :**
    - 🟢 0-50 : Bon
    - 🟡 51-100 : Moyen  
    - 🔴 101+ : Mauvais
    """)
    
    st.divider()
    st.markdown("*Modèle : Random Forest Regressor*")
    st.markdown(f"*Features : {len(features)}*")

# 8. Instructions d'installation
if st.sidebar.button("🔄 Recréer le modèle"):

    st.sidebar.info("Exécutez 'python train_model.py' dans votre terminal")

