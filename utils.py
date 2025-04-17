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
    """
    Charge le modèle DeepSurv pré-entraîné.
    """
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        # Définition de la fonction de perte utilisée lors de l'entraînement DeepSurv (Cox Loss)
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
    """
    Encode les variables cliniques :
    - Pour 'AGE', on conserve la valeur numérique.
    - Pour les autres, "OUI" devient 1 et toute autre valeur 0.
    """
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = v
        else:
            encoded[k] = 1 if v.upper() == "OUI" else 0
    return pd.DataFrame([encoded])

def predict_survival(model, data):
    """
    Effectue la prédiction du temps de survie avec le modèle DeepSurv.
    
    Correction : on transforme la prédiction brute (risque) en une estimation de la survie médiane.
    En utilisant l'hypothèse d'une distribution exponentielle, la survie médiane est estimée par :
        survie = baseline_median * exp(-risk)
    Ainsi, si tous les champs sont "Non" (risk proche de 0), la survie sera d'environ 60 mois.
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
    """
    Nettoie la prédiction pour éviter les valeurs négatives.
    Pour DeepSurv, on s'assure d'avoir au moins 1 mois.
    """
    try:
        pred_val = float(prediction)
    except Exception:
        pred_val = 0
    return max(pred_val, 1)

def save_new_patient(new_patient_data):
    """
    Enregistre les informations d'un nouveau patient dans le fichier Excel
    avec les valeurs booléennes converties en 'OUI' ou 'NON'.
    Déclenche également l'actualisation incrémentale du modèle.
    """

    # Fonction de conversion booléen/nombre → OUI/NON
    def bool_to_oui_non(val):
        if isinstance(val, (int, float)):
            return "OUI" if val == 1 else "NON"
        return val

    # Charger les données existantes
    df = load_data()

    # Préparer les nouvelles données avec conversion
    new_df = pd.DataFrame([{
        k: bool_to_oui_non(v) if k != "AGE" else v
        for k, v in new_patient_data.items()
    }])

    # Convertir tous les types de données à des types compatibles avant d'enregistrer
    for col in new_df.columns:
        if new_df[col].dtype == "object":
            new_df[col] = new_df[col].apply(str)  # Convertir tout en chaîne de caractères si nécessaire
        elif new_df[col].dtype == "bool":
            new_df[col] = new_df[col].astype(int)  # Convertir les booléens en entiers (0/1)

    # Ajouter et sauvegarder
    df = pd.concat([df, new_df], ignore_index=True)
    try:
        # Convertir tout le DataFrame en types compatibles avant de l'enregistrer dans Excel
        df = df.apply(pd.to_numeric, errors='ignore')  # Convertir tout en numérique si possible
        df.to_excel(DATA_PATH, index=False)
        st.success("✅ Les informations du nouveau patient ont été enregistrées.")
        load_data.clear()  # Vider le cache
        update_deepsurv_model()  # Mise à jour du modèle
    except Exception as e:
        st.error(f"❌ Erreur lors de l'enregistrement des données : {e}")


def update_deepsurv_model():
    """
    Recharge l'ensemble des données et ajuste (fine-tune) le modèle DeepSurv 
    avec les nouvelles informations patient.
    
    Hypothèses :
    - La base de données contient toutes les variables définies dans FEATURE_CONFIG.
    - La colonne 'Tempsdesuivi' contient le temps de suivi (durée) en mois.
    - La colonne 'Deces' est codée par 'OUI' pour l'événement survenu et toute autre valeur pour un censuré.
    
    Cette fonction effectue un entraînement supplémentaire (fine-tuning) sur l'ensemble des données.
    """
    df = load_data()
    if df.empty:
        st.warning("La base de données est vide. Impossible de mettre à jour le modèle.")
        return

    # Préparation des features
    feature_cols = list(FEATURE_CONFIG.keys())
    X = df[feature_cols].copy()
    for col in feature_cols:
        if col != "AGE":
            X[col] = X[col].apply(lambda x: 1 if str(x).upper() == "OUI" else 0)

    # Préparation des cibles
    # La première colonne de y correspond à l'événement : 1 si 'Deces' vaut "OUI", 0 sinon.
    # La deuxième colonne correspond à la durée de suivi (Tempsdesuivi).
    y_duration = df["Tempsdesuivi"].values
    y_event = df["Deces"].apply(lambda x: 1 if str(x).upper() == "OUI" else 0).values
    y = np.column_stack([y_event, y_duration])

    # Chargement et compilation du modèle DeepSurv
    model = load_model(MODELS["DeepSurv"])
    if model is None:
        st.error("❌ Impossible de charger le modèle DeepSurv.")
        return

    # Fine-tuning du modèle avec les nouvelles données
    model.compile(optimizer=adam, loss="cox_loss")
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)

    # Sauvegarde du modèle fine-tuné
    model.save(MODELS["DeepSurv"])
    st.success("✅ Le modèle DeepSurv a été mis à jour avec succès.")

