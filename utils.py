import os
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model as tf_load_model
import streamlit as st
import plotly.express as px

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
    "DeepSurv": "models/deepsurv.keras",
}

# Configuration des variables
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

# Fonctions utilitaires

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
    """
    Charge un modèle pré-entraîné.
    Pour les modèles Keras (.keras ou .h5) on utilise tf.keras.models.load_model.
    """
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None
    return tf_load_model(model_path)

def encode_features(inputs):
    """
    Encode les variables.
    Pour 'AGE', on conserve la valeur numérique.
    Pour les autres, "OUI" devient 1 et toute autre valeur 0.
    """
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = v
        else:
            encoded[k] = 1 if v.upper() == "OUI" else 0
    return pd.DataFrame([encoded])

def predict_survival(model, data, model_name):
    """
    Effectue la prédiction du temps de survie selon le type de modèle.
    """
    if hasattr(model, "predict_median"):
        pred = model.predict_median(data)
        if hasattr(pred, '__iter__'):
            return pred.iloc[0] if isinstance(pred, pd.Series) else pred[0]
        return pred
    elif hasattr(model, "predict"):
        prediction = model.predict(data)
        if isinstance(prediction, np.ndarray):
            if prediction.ndim == 2:
                return prediction[0][0]
            return prediction[0]
        return prediction
    else:
        raise ValueError(f"Le modèle {model_name} ne supporte pas la prédiction de survie.")

def clean_prediction(prediction, model_name):
    """
    Nettoie la prédiction pour éviter les valeurs négatives.
    """
    try:
        pred_val = float(prediction)
    except Exception:
        pred_val = 0
    if model_name == "DeepSurv":
        return max(pred_val, 1)
    return pred_val

def retrain_deepsurv_model(df, model_path=MODELS["DeepSurv"]):
    """
    Réentraîne le modèle DeepSurv avec les nouvelles données.
    """
    model = load_model(model_path)
    if model is None:
        st.error("❌ Le modèle DeepSurv est introuvable.")
        return None

    # Exemple d'ajustement: prédiction sur les nouvelles données pour DeepSurv
    # Divisez vos données en features et cible
    X = df[FEATURE_CONFIG.keys()]  # Modifiez ceci selon vos colonnes de caractéristiques
    y = df['survival_time']  # Assurez-vous que vous avez la colonne de durée de survie
    event = df['event']  # Assurez-vous que vous avez la colonne d'événements (1 pour événement, 0 pour censuré)

    # Apprentissage sur les nouvelles données
    model.fit(X, y, event, epochs=10, batch_size=32, verbose=1)

    # Sauvegarde du modèle mis à jour
    model.save(model_path)
    st.success("✅ Le modèle DeepSurv a été réentraîné avec succès.")
    return model

def save_new_patient(new_patient_data):
    """
    Enregistre les informations d'un nouveau patient dans le fichier Excel et réentraîne le modèle.
    """
    df = load_data()
    new_df = pd.DataFrame([new_patient_data])
    df = pd.concat([df, new_df], ignore_index=True)
    
    try:
        # Sauvegarde des nouvelles données dans le fichier
        df.to_excel(DATA_PATH, index=False)
        st.success("Les informations du nouveau patient ont été enregistrées.")
        
        # Réentraîner le modèle avec les nouvelles données
        retrain_deepsurv_model(df)
        
        load_data.clear()  # Nettoyer le cache des données
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement des données : {e}")
