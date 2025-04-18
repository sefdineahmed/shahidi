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
    "CoxPH": "models/coxph.joblib"
}

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

# --- Chargement des données ---
@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    else:
        st.error(f"❌ Fichier introuvable : {DATA_PATH}")
        return pd.DataFrame()

# --- Fonction de perte Cox personnalisée ---
def cox_loss(y_true, y_pred):
    event = tf.cast(y_true[:, 0], dtype=tf.float32)
    risk = y_pred[:, 0]
    log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
    loss = -tf.reduce_mean((risk - log_risk) * event)
    return loss

# --- Chargement du modèle DeepSurv ---
@st.cache_resource(show_spinner=False)
def load_model(model_path):
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        return tf_load_model(model_path, custom_objects={"cox_loss": cox_loss})
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None

# --- Encodage des caractéristiques ---
def encode_features(inputs):
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = v
        else:
            encoded[k] = 1 if str(v).upper() == "OUI" else 0
    return pd.DataFrame([encoded])

# --- Calibration : déterminer les seuils de survie ---
def calibrate_median_survival_by_risk_group(model, X, y, n_groups=3):
    risk_scores = model.predict(X).flatten()
    df = pd.DataFrame({
        'risk': risk_scores,
        'event': y[:, 0],
        'time': y[:, 1]
    })

    df['risk_group'] = pd.qcut(df['risk'], q=n_groups, labels=False, duplicates='drop')
    median_by_group = df.groupby('risk_group')['time'].median().to_dict()
    thresholds = np.quantile(df['risk'], q=np.linspace(0, 1, n_groups+1)[1:-1])
    return thresholds, median_by_group

# --- Prédiction du temps de survie ---
def predict_survival(model, data, thresholds=None, median_by_group=None):
    risk_score = float(model.predict(data).flatten()[0])

    if thresholds is None or median_by_group is None:
        # Estimation simpliste si calibration non disponible
        baseline_median = 60.0  # durée médiane arbitraire
        return baseline_median * np.exp(-risk_score)
    else:
        group = sum(risk_score > t for t in thresholds)
        return median_by_group.get(group, 1.0)

# --- Nettoyage des prédictions (évitent les valeurs négatives ou NaN) ---
def clean_prediction(prediction):
    try:
        pred_val = float(prediction)
    except Exception:
        pred_val = 0
    return max(pred_val, 1)

# --- Sauvegarde d'un nouveau patient ---
def save_new_patient(new_patient_data):
    def bool_to_oui_non(val):
        if isinstance(val, (int, float)):
            return "OUI" if val == 1 else "NON"
        return str(val)

    df = load_data()
    new_df = pd.DataFrame([{
        k: bool_to_oui_non(v) if k != "AGE" else v
        for k, v in new_patient_data.items()
    }])
    for col in new_df.columns:
        if new_df[col].dtype == "object":
            new_df[col] = new_df[col].astype(str)

    df = pd.concat([df, new_df], ignore_index=True)

    try:
        df.to_excel(DATA_PATH, index=False)
        st.success("✅ Les informations du nouveau patient ont été enregistrées.")
        load_data.clear()
        update_deepsurv_model()
    except Exception as e:
        st.error(f"❌ Erreur lors de l'enregistrement des données : {e}")

# --- Mise à jour du modèle DeepSurv avec les nouvelles données ---
def update_deepsurv_model():
    df = load_data()
    if df.empty:
        st.warning("La base de données est vide. Impossible de mettre à jour le modèle.")
        return

    feature_cols = list(FEATURE_CONFIG.keys())
    X = df[feature_cols].copy()
    for col in feature_cols:
        if col != "AGE":
            X[col] = X[col].apply(lambda x: 1 if str(x).upper() == "OUI" else 0)

    y_duration = df["Tempsdesuivi"].astype(float).values
    y_event = df["Deces"].apply(lambda x: 1 if str(x).upper() == "OUI" else 0).values
    y = np.column_stack([y_event, y_duration])

    model = load_model(MODELS["DeepSurv"])
    if model is None:
        st.error("❌ Impossible de charger le modèle DeepSurv.")
        return

    model.compile(optimizer=adam, loss=cox_loss)
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)
    model.save(MODELS["DeepSurv"])
    st.success("✅ Le modèle DeepSurv a été mis à jour avec succès.")
