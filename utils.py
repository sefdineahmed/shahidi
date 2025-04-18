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

# Chemins des ressources
DATA_PATH = "data/data.xlsx"
LOGO_PATH = "assets/background.jpeg"

# Modèles disponibles
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

# Définition des membres de l'équipe
TEAM_MEMBERS = [
    {
        "name": "Pr. Aba Diop",
        "Etablissement": "Université Alioune Diop de Bamby",
        "role": "Maître de Conférences",
        "email": "aba.diop@example.com",
        "linkedin": "https://linkedin.com/in/abadiop",
        "photo": "assets/team/aba.jpeg"
    },
    {
        "name": "PhD. Idrissa Sy",
        "Etablissement": "Université Alioune Diop de Bamby",
        "role": "Enseignant Chercheur",
        "email": "idrissa.sy@example.com",
        "linkedin": "https://linkedin.com/in/idrissasy",
        "photo": "assets/team/sy.jpeg"
    },
    {
        "name": "M. Ahmed Sefdine",
        "Etablissement": "Université Alioune Diop de Bamby",
        "role": "Étudiant",
        "email": "ahmed.sefdine@example.com",
        "linkedin": "https://linkedin.com/in/sefdineahmed",
        "photo": "assets/team/sefdine.jpeg"
    }
]

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
    """Charge le modèle sélectionné (DeepSurv ou CoxPH)"""
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    try:
        if model_path.endswith(".keras"):
            # Chargement DeepSurv avec fonction de perte personnalisée
            def cox_loss(y_true, y_pred):
                event = tf.cast(y_true[:, 0], dtype=tf.float32)
                risk = y_pred[:, 0]
                log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True)
                loss = -tf.reduce_mean((risk - log_risk) * event)
                return loss
            return tf_load_model(model_path, custom_objects={"cox_loss": cox_loss})
        elif model_path.endswith(".joblib"):
            # Chargement CoxPH avec joblib
            return joblib.load(model_path)
        else:
            st.error("Format de modèle non supporté")
            return None
    except Exception as e:
        st.error(f"❌ Erreur de chargement du modèle : {e}")
        return None

def encode_features(inputs):
    """
    Encode les variables cliniques :
    - 'AGE' : valeur numérique
    - Autres : 1 pour "OUI", 0 sinon
    """
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = v
        else:
            encoded[k] = 1 if v.upper() == "OUI" else 0
    return pd.DataFrame([encoded])

def predict_survival(model, data):
    """Prédiction générique pour les deux modèles"""
    try:
        # Prédiction selon le type de modèle
        if isinstance(model, tf.keras.Model):
            # DeepSurv
            raw_pred = model.predict(data)
            raw_pred = raw_pred[0][0] if raw_pred.ndim == 2 else raw_pred[0]
        else:
            # CoxPH (format sklearn)
            raw_pred = model.predict(data.values)
            raw_pred = raw_pred[0] if isinstance(raw_pred, np.ndarray) else raw_pred

        # Conversion risque -> survie médiane
        baseline_median = 60.0
        est_time = baseline_median * np.exp(-raw_pred)
        return est_time
    except Exception as e:
        st.error(f"Erreur de prédiction : {e}")
        return None

def clean_prediction(prediction):
    """Nettoyage des prédictions"""
    try:
        pred_val = float(prediction)
    except Exception:
        pred_val = 0
    return max(pred_val, 1)

def save_new_patient(new_patient_data):
    """Sauvegarde un nouveau patient et met à jour les modèles"""
    df = load_data()
    new_df = pd.DataFrame([new_patient_data])
    df = pd.concat([df, new_df], ignore_index=True)
    try:
        df.to_excel(DATA_PATH, index=False)
        st.success("Patient enregistré avec succès !")
        load_data.clear()
        update_deepsurv_model()
    except Exception as e:
        st.error(f"Erreur d'enregistrement : {e}")

def update_deepsurv_model():
    """Mise à jour du modèle DeepSurv avec toutes les données"""
    df = load_data()
    if df.empty:
        st.warning("Base de données vide !")
        return

    # Préparation des données
    feature_cols = list(FEATURE_CONFIG.keys())
    X = df[feature_cols].copy()
    for col in feature_cols:
        if col != "AGE":
            X[col] = X[col].apply(lambda x: 1 if str(x).upper() == "OUI" else 0)

    y_duration = df["Tempsdesuivi"].values
    y_event = df["Deces"].apply(lambda x: 1 if str(x).upper() == "OUI" else 0).values
    y = np.column_stack([y_event, y_duration])

    # Chargement et entraînement
    model = load_model(MODELS["DeepSurv"])
    if model is None:
        return

    def cox_loss(y_true, y_pred):
        event = tf.cast(y_true[:, 0], dtype=tf.float32)
        risk = y_pred[:, 0]
        log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True)
        loss = -tf.reduce_mean((risk - log_risk) * event)
        return loss

    model.compile(optimizer=adam, loss=cox_loss)
    model.fit(X, y, epochs=10, batch_size=32)
    model.save(MODELS["DeepSurv"])
    st.success("Modèle DeepSurv mis à jour !")

# Fonction d'affichage des résultats
def display_results(prediction):
    """Affiche les résultats de prédiction de manière visuelle"""
    months = clean_prediction(prediction)
    fig = px.bar(
        x=["Survie médiane estimée"],
        y=[months],
        labels={'x': '', 'y': 'Mois'},
        color_discrete_sequence=['#2ecc71'],
        text_auto=True
    )
    fig.update_layout(
        title="Résultat de la prédiction",
        showlegend=False,
        yaxis_range=[0, 120]
    )
    st.plotly_chart(fig)
    st.info(f"**Estimation finale :** {months:.1f} mois")
