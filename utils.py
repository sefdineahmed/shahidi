import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
import plotly.express as px
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model as tf_load_model

# Configuration pour scikit-learn
try:
    from sklearn.base import BaseEstimator
    if not hasattr(BaseEstimator, "sklearn_tags"):
        @property
        def sklearn_tags(self):
            return {}
        BaseEstimator.sklearn_tags = sklearn_tags
except Exception as e:
    pass

# Définition globale de la fonction de perte
def cox_loss(y_true, y_pred):
    event = tf.cast(y_true[:, 0], dtype=tf.float32)
    risk = y_pred[:, 0]
    log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
    return -tf.reduce_mean((risk - log_risk) * event)

# Configuration
adam = Adam()
DATA_PATH = "data/data.xlsx"
LOGO_PATH = "assets/background.jpeg"
MODELS = {
    "DeepSurv": "models/deepsurv.keras",
    "CoxPH": "models/coxph.joblib"
}

FEATURE_CONFIG = {
    "AGE": "Âge",
    "Cardiopathie": "Cardiopathie",
    # ... (autres features identiques)
}

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
    """Charge le modèle selon son format"""
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        if model_path.endswith(".joblib"):
            return joblib.load(model_path)
        elif model_path.endswith(".keras"):
            return tf_load_model(model_path, custom_objects={"cox_loss": cox_loss})
        else:
            raise ValueError("Format de modèle non supporté")
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None

def encode_features(inputs):
    """Encode les features pour la prédiction"""
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = float(v)
        else:
            encoded[k] = 1.0 if str(v).upper() == "OUI" else 0.0
    return pd.DataFrame([encoded], dtype=float)

def predict_survival(model, data):
    """Effectue la prédiction selon le type de modèle"""
    try:
        # Prédiction DeepSurv
        if isinstance(model, tf.keras.Model):
            raw_pred = model.predict(data)
            raw_pred = raw_pred[0][0] if raw_pred.ndim == 2 else raw_pred[0]
            return 60.0 * np.exp(-raw_pred)
        
        # Prédiction CoxPH
        else:
            risk_score = model.predict_proba(data)
            return np.median(-np.log(risk_score) / 0.1)
            
    except Exception as e:
        raise ValueError(f"Erreur de prédiction : {str(e)}")

def clean_prediction(prediction):
    """Nettoie la prédiction"""
    try:
        return max(float(prediction), 1.0)
    except:
        return 1.0

def save_new_patient(new_patient_data):
    """Enregistre les nouvelles données patient"""
    df = load_data()
    new_df = pd.DataFrame([new_patient_data])
    
    for col in new_df.columns:
        if col != "AGE":
            new_df[col] = new_df[col].apply(lambda x: "OUI" if str(x).upper() == "OUI" else "NON")

    try:
        pd.concat([df, new_df]).to_excel(DATA_PATH, index=False)
        load_data.clear()
        if "DeepSurv" in MODELS.values():
            update_deepsurv_model()
        st.success("Patient enregistré avec succès!")
    except Exception as e:
        st.error(f"Erreur d'enregistrement : {e}")

def update_deepsurv_model():
    """Mise à jour incrémentale du modèle DeepSurv"""
    df = load_data()
    if df.empty:
        return

    model = load_model(MODELS["DeepSurv"])
    if not isinstance(model, tf.keras.Model):
        st.error("Mise à jour réservée à DeepSurv")
        return

    X = df[FEATURE_CONFIG.keys()].applymap(lambda x: 1 if str(x).upper() == "OUI" else 0 if x != "AGE" else x)
    y = np.column_stack([df["Deces"].map({"OUI":1, "NON":0}), df["Tempsdesuivi"]])

    model.compile(optimizer=adam, loss=cox_loss)
    model.fit(X, y, epochs=10, verbose=0)
    model.save(MODELS["DeepSurv"])
