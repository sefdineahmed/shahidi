import os
import pandas as pd
import joblib
import tensorflow as tf
import numpy as np
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
    "Cox PH": "models/coxph.joblib",
    "RSF": "models/rsf.joblib",
    "DeepSurv": "models/deepsurv.keras",
    "GBST": "models/gbst.joblib"
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

# Définition des membres de l'équipe
TEAM_MEMBERS = [
    {
        "name": "Pr. Aba Diop",
        "Etablissement" : "Université Alioune Diop de Bamby",
        "role": "Maître de Conférences",
        "email": "aba.diop@example.com",
        "linkedin": "https://linkedin.com/in/abadiop",
        "photo": "assets/team/aba.jpeg"
    },
    {
        "name": "PhD. Idrissa Sy",
        "Etablissement" : "Université Alioune Diop de Bamby",
        "role": "Enseignant Chercheur",
        "email": "idrissa.sy@example.com",
        "linkedin": "https://linkedin.com/in/idrissasy",
        "photo": "assets/team/sy.jpeg"
    },
    {
        "name": "M. Ahmed Sefdine",
        "Etablissement" : "Université Alioune Diop de Bamby",
        "role": "Étudiant",
        "email": "ahmed.sefdine@example.com",
        "linkedin": "https://linkedin.com/in/sefdineahmed",
        "photo": "assets/team/sefdine.jpeg"
    }
]

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
    Pour les autres, joblib.load.
    """
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        _, ext = os.path.splitext(model_path)
        if ext in ['.keras', '.h5']:
            def cox_loss(y_true, y_pred):
                event = tf.cast(y_true[:, 0], dtype=tf.float32)
                risk = y_pred[:, 0]
                log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
                loss = -tf.reduce_mean((risk - log_risk) * event)
                return loss
            return tf_load_model(model_path, custom_objects={"cox_loss": cox_loss})
        else:
            return joblib.load(model_path)
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None

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
    if model_name in ["Cox PH", "RSF", "GBST"]:
        return max(pred_val, 0)
    elif model_name == "DeepSurv":
        return max(pred_val, 1)
    else:
        return pred_val

def save_new_patient(new_patient_data):
    """
    Enregistre les informations d'un nouveau patient dans le fichier Excel.
    """
    df = load_data()
    new_df = pd.DataFrame([new_patient_data])
    df = pd.concat([df, new_df], ignore_index=True)
    try:
        df.to_excel(DATA_PATH, index=False)
        st.success("Les informations du nouveau patient ont été enregistrées.")
        load_data.clear()
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement des données : {e}")
