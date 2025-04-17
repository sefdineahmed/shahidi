import os
import joblib
import random
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
import plotly.express as px
from tensorflow.keras.activations import relu, tanh
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model as tf_load_model

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

# Définir l'optimiseur
adam = Adam()

# Chemin vers les ressources
DATA_PATH = "data/data.xlsx"
LOGO_PATH = "assets/background.jpeg"

# Pour ce projet, nous utilisons uniquement le modèle DeepSurv
MODELS = {
    "DeepSurv": "models/deepsurv.keras",
    "CoxPH": "models/coxph.joblib"
}

# Configuration des variables cliniques
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

# -----------------------
# Fonctions utilitaires
# -----------------------

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
    """Charge le modèle DeepSurv pré-entraîné."""

    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        def cox_loss(y_true, y_pred):
            event = tf.cast(y_true[:, 0], dtype=tf.float32)
            risk = y_pred[:, 0]
            log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
            loss = -tf.reduce_mean((risk - log_risk) * event)
            return loss

        return tf_load_model(model_path, custom_objects={"cox_loss": cox_loss})
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None

def encode_features(inputs):
    """Encode les variables cliniques."""
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = v
        else:
            encoded[k] = 1 if v.upper() == "OUI" else 0
    return pd.DataFrame([encoded])

def predict_survival(model, data):
    """
    Prédit la survie médiane estimée à partir du risque avec DeepSurv.
    """
    if hasattr(model, "predict"):
        raw_pred = model.predict(data)
        if isinstance(raw_pred, np.ndarray):
            if raw_pred.ndim == 2:
                raw_pred = raw_pred[0][0]
            else:
                raw_pred = raw_pred[0]
        baseline_median = 60.0
        est_time = baseline_median * np.exp(-raw_pred)
        return est_time
    else:
        raise ValueError("Le modèle DeepSurv ne supporte pas la prédiction.")

def clean_prediction(prediction):
    """Nettoie la prédiction pour éviter les valeurs négatives."""
    try:
        pred_val = float(prediction)
    except Exception:
        pred_val = 0
    return max(pred_val, 1)

def save_new_patient(new_patient_data):
    """
    Enregistre les informations d'un nouveau patient dans le fichier Excel.
    """

    def bool_to_oui_non(val):
        if isinstance(val, (int, float)):
            return "OUI" if val == 1 else "NON"
        return val

    df = load_data()

    # Préparer les nouvelles données
    new_df = pd.DataFrame([{
        k: bool_to_oui_non(v) if k != "AGE" else v
        for k, v in new_patient_data.items()
    }])

    # Forcer tous les types en chaînes ou numériques uniquement
    for col in new_df.columns:
        if new_df[col].dtype == "object":
            new_df[col] = new_df[col].astype(str)
        elif new_df[col].dtype == "bool":
            new_df[col] = new_df[col].astype(int)

    df = pd.concat([df, new_df], ignore_index=True)

    try:
        # Nettoyage des types avant sauvegarde
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].astype(str)
            elif df[col].dtype == "bool":
                df[col] = df[col].astype(int)

        df.to_excel(DATA_PATH, index=False)
        st.success("✅ Les informations du nouveau patient ont été enregistrées.")
        load_data.clear()
        update_deepsurv_model()

    except Exception as e:
        st.error(f"❌ Erreur lors de l'enregistrement des données : {e}")
        st.write("Types de colonnes :", df.dtypes.to_dict())

def update_deepsurv_model():
    """
    Met à jour le modèle DeepSurv avec les nouvelles données patient.
    """
    df = load_data()
    if df.empty:
        st.warning("La base de données est vide. Impossible de mettre à jour le modèle.")
        return

    feature_cols = list(FEATURE_CONFIG.keys())
    X = df[feature_cols].copy()
    for col in feature_cols:
        if col != "AGE":
            X[col] = X[col].apply(lambda x: 1 if str(x).upper() == "OUI" else 0)

    y_duration = df["Tempsdesuivi"].values
    y_event = df["Deces"].apply(lambda x: 1 if str(x).upper() == "OUI" else 0).values
    y = np.column_stack([y_event, y_duration])

    model = load_model(MODELS["DeepSurv"])
    if model is None:
        st.error("❌ Impossible de charger le modèle DeepSurv.")
        return

    model.compile(optimizer=adam, loss="cox_loss")
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)

    model.save(MODELS["DeepSurv"])
    st.success("✅ Le modèle DeepSurv a été mis à jour avec succès.")
