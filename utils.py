import os
import numpy as np  
import pandas as pd
import joblib
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model as tf_load_model
import streamlit as st
import plotly.express as px
from onglets.modelisation import modelisation

# --- Patch scikit-learn pour éviter l'erreur 'sklearn_tags' ---
try:
    from sklearn.base import BaseEstimator
    if not hasattr(BaseEstimator, "sklearn_tags"):
        @property
        def sklearn_tags(self):
            return {}
        BaseEstimator.sklearn_tags = sklearn_tags
except Exception as e:
    pass

# Chemins vers les ressources
DATA_PATH = "data/data.xlsx"
LOGO_PATH = "assets/background.jpeg"

# Configuration des modèles
MODELS = {
    "DeepSurv": "models/deepsurv.keras"
}

# Définition des variables des caractéristiques
FEATURE_CONFIG = {
    "AGE": "Âge",
    "Cardiopathie": "Cardiopathie",
    "Ulceregastrique": "Ulcère gastrique",
    "Douleurepigastrique": "Douleur épigastrique",
    "Ulcero-bourgeonnant": "Lésion ulcéro-bourgeonnante",
    "Denitrution": "Dénutrition",
    "Tabac": "Tabagisme actif",
    "Mucineux": "Type mucineux",
    "Infiltrant": "Type infiltrant",
    "Stenosant": "Type sténosant",
    "Metastases": "Métastases",
    "Adenopathie": "Adénopathie",
}

# --- Fonctions Utilitaires ---
@st.cache_data(show_spinner=False)
def load_data():
    """Charge les données depuis le fichier Excel."""
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    else:
        st.error(f"❌ Fichier introuvable : {DATA_PATH}")
        return pd.DataFrame()

@st.cache_resource(show_spinner=False)
def load_model(model_path):
    """Charge un modèle pré-entraîné."""
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        return tf_load_model(model_path)
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None

def encode_features(inputs):
    """Encode les variables. Pour 'AGE', on conserve la valeur numérique."""
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = v
        else:
            encoded[k] = 1 if v.upper() == "OUI" else 0
    return pd.DataFrame([encoded])

def predict_survival(model, data):
    """Effectue la prédiction du temps de survie selon le type de modèle."""
    prediction = model.predict(data)
    return prediction[0][0]

def clean_prediction(prediction):
    """Nettoie la prédiction pour éviter les valeurs négatives."""
    return max(prediction, 1)

def save_new_patient(new_patient_data):
    """Enregistre les informations d'un nouveau patient dans le fichier Excel."""
    df = load_data()
    new_df = pd.DataFrame([new_patient_data])
    df = pd.concat([df, new_df], ignore_index=True)
    try:
        df.to_excel(DATA_PATH, index=False)
        st.success("Les informations du nouveau patient ont été enregistrées.")
        load_data.clear()
        retrain_model(df)  # Réentraîner le modèle après ajout des nouvelles données
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement des données : {e}")

def retrain_model(data):
    """Réentraîne le modèle DeepSurv avec les nouvelles données."""
    # Préparation des données
    X = data.drop(columns=["Tempsdesuivi", "Deces"])
    y = data["Tempsdesuivi"]

    # Normalisation des données
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Chargement du modèle DeepSurv existant
    model = load_model(MODELS["DeepSurv"])

    # Réentraînement du modèle
    model.fit(X_scaled, y, epochs=10, batch_size=32)

    # Sauvegarder le modèle réentrainé
    model.save(MODELS["DeepSurv"])
    st.success("Le modèle a été réentraîné avec les nouvelles données.")
