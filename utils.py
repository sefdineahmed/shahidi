# utils.py

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model as tf_load_model

# --- Correction compatibilité sklearn ---
try:
    from sklearn.base import BaseEstimator
    if not hasattr(BaseEstimator, "sklearn_tags"):
        @property
        def sklearn_tags(self):
            return {}
        BaseEstimator.sklearn_tags = sklearn_tags
except Exception:
    pass

# --- Constantes ---
DATA_PATH = "data/data.xlsx"
LOGO_PATH = "assets/background.jpeg"
adam = Adam()

MODELS = {
    "DeepSurv": "models/deepsurv.keras",
    "CoxPH":   "models/coxph.joblib"
}

FEATURE_CONFIG = {
    "AGE":               "Âge",
    "Cardiopathie":      "Cardiopathie",
    "Ulceregastrique":   "Ulcère gastrique",
    "Douleurepigastrique": "Douleur épigastrique",
    "Ulcero-bourgeonnant": "Lésion ulcéro-bourgeonnante",
    "Denitrution":       "Dénutrition",
    "Tabac":             "Tabagisme actif",
    "Mucineux":          "Type mucineux",
    "Infiltrant":        "Type infiltrant",
    "Stenosant":         "Type sténosant",
    "Metastases":        "Métastases",
    "Adenopathie":       "Adénopathie",
}

# --- Chargement des données ---
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    st.error(f"❌ Fichier introuvable : {DATA_PATH}")
    return pd.DataFrame()

# --- Chargement du modèle DeepSurv ---
@st.cache_resource(show_spinner=False)
def load_deepsurv_model(path: str):
    if not os.path.exists(path):
        st.error(f"❌ Modèle introuvable : {path}")
        return None
    try:
        return tf_load_model(path, custom_objects={"cox_loss": cox_loss})
    except Exception as e:
        st.error(f"❌ Erreur chargement DeepSurv : {e}")
        return None

# --- Chargement du modèle CoxPH ---
@st.cache_resource(show_spinner=False)
def load_cox_model(path: str):
    if not os.path.exists(path):
        st.error(f"❌ Modèle introuvable : {path}")
        return None
    try:
        return joblib.load(path)
    except Exception as e:
        st.error(f"❌ Erreur chargement CoxPH : {e}")
        return None

# --- Custom loss pour DeepSurv ---
def cox_loss(y_true, y_pred):
    event = tf.cast(y_true[:, 0], tf.float32)
    risk  = y_pred[:, 0]
    log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
    return -tf.reduce_mean((risk - log_risk) * event)

# --- Encodage des inputs utilisateur en DataFrame ---
def encode_features(inputs: dict) -> pd.DataFrame:
    enc = {}
    for k, v in inputs.items():
        enc[k] = v if k == "AGE" else (1 if str(v).upper() == "OUI" else 0)
    return pd.DataFrame([enc])

# --- Extraction des scores de risque (DeepSurv ou CoxPH) ---
def get_risk_scores(model, X: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict"):
        scores = model.predict(X)
    elif hasattr(model, "predict_partial_hazard"):
        # pour lifelines.CoxPHFitter
        scores = model.predict_partial_hazard(X)
    else:
        raise AttributeError("Modèle sans méthode de prédiction de risque reconnue.")
    return np.array(scores).reshape(-1)

# --- Calibration : thresholds et médianes par groupe de risque ---
def calibrate_median_survival_by_risk_group(model, X: pd.DataFrame, y: np.ndarray, n_groups: int = 3):
    risks = get_risk_scores(model, X)
    df = pd.DataFrame({
        "risk":  risks,
        "event": y[:, 0],
        "time":  y[:, 1]
    })
    df["risk_group"] = pd.qcut(df["risk"], q=n_groups, labels=False, duplicates="drop")
    medians = df.groupby("risk_group")["time"].median().to_dict()
    thresholds = np.quantile(df["risk"], q=np.linspace(0, 1, n_groups + 1)[1:-1])
    return thresholds, medians

# --- Prédiction du temps de survie d'un seul patient ---
def predict_survival(model, data: pd.DataFrame, thresholds=None, median_by_group=None) -> float:
    risk = float(get_risk_scores(model, data)[0])
    if thresholds is None or median_by_group is None:
        # fallback simple
        baseline = 60.0
        return baseline * np.exp(-risk)
    group = sum(risk > t for t in thresholds)
    return median_by_group.get(group, baseline)

# --- Nettoyage final de la prédiction ---
def clean_prediction(pred: float) -> float:
    try:
        p = float(pred)
    except Exception:
        p = 0.0
    return max(p, 1.0)

# --- Sauvegarde d'une nouvelle entrée patient ---
def save_new_patient(new_patient: dict, filename: str = DATA_PATH):
    new_clean = {
        k: (float(v) if isinstance(v, (int, float)) else str(v))
        for k, v in new_patient.items()
    }
    entry = pd.DataFrame([new_clean])
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        df = pd.concat([df, entry], ignore_index=True)
    else:
        df = entry
    df.to_excel(filename, index=False)
