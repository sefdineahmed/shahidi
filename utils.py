import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
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
except:
    pass

# Définir l'optimiseur
adam = Adam()

# Définir globalement la fonction de perte Cox pour Keras
def cox_loss(y_true, y_pred):
    event = tf.cast(y_true[:, 0], dtype=tf.float32)
    risk = y_pred[:, 0]
    log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
    return -tf.reduce_mean((risk - log_risk) * event)

# Chemin vers les ressources
DATA_PATH = "data/data.xlsx"
LOGO_PATH = "assets/background.jpeg"
# Modèles disponibles
MODELS = {
    "DeepSurv": "models/deepsurv.keras",
    "CoxPH":    "models/coxph.joblib"
}

FEATURE_CONFIG = {
    "AGE": "Âge",
    "Cardiopathie": "Cardiopathie",
    "Ulceregastrique": "Ul­cère gastrique",
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

@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    st.error(f"❌ Fichier introuvable : {DATA_PATH}")
    return pd.DataFrame()

@st.cache_resource(show_spinner=False)
def load_model(model_path):
    """
    Charge un modèle DeepSurv (.keras) ou CoxPH (.joblib).
    """
    if not os.path.exists(model_path):
        st.error(f"❌ Modèle introuvable : {model_path}")
        return None

    ext = os.path.splitext(model_path)[1].lower()
    try:
        if ext == ".joblib":
            # Chargement du CoxPH
            return joblib.load(model_path)
        else:
            # Chargement du DeepSurv Keras
            return tf_load_model(model_path, custom_objects={"cox_loss": cox_loss})
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        return None

def encode_features(inputs):
    """
    Encode les inputs pour le modèle :
     - AGE → float
     - Autres → 1.0 si "OUI", sinon 0.0
    """
    encoded = {}
    for k, v in inputs.items():
        if k == "AGE":
            encoded[k] = float(v)
        else:
            encoded[k] = 1.0 if str(v).strip().upper() == "OUI" else 0.0
    return pd.DataFrame([encoded], dtype=float)

def predict_survival(model, data):
    """
    Prédit le temps médian de survie :
     - Pour DeepSurv (Keras), on applique exp(-risk)
     - Pour CoxPH, on suppose que model.predict renvoie un score de risque
    """
    if model is None:
        raise ValueError("Modèle non chargé.")

    # DeepSurv : modèle Keras
    if hasattr(model, "predict") and isinstance(model, tf.keras.Model):
        raw = model.predict(data)
        raw = float(raw.flatten()[0])
    # CoxPH : modèle joblib (scikit-like)
    elif hasattr(model, "predict"):
        # predict renvoie un array de risque
        raw_arr = model.predict(data)
        raw = float(np.ravel(raw_arr)[0])
    else:
        raise ValueError("Modèle non compatible pour la prédiction.")

    # Conversion en survie médiane (exponentielle autour de 60 mois)
    baseline = 60.0
    return baseline * np.exp(-raw)

def clean_prediction(pred):
    """
    Empêche les valeurs < 1 mois.
    """
    try:
        val = float(pred)
    except:
        val = 0.0
    return max(val, 1.0)

def save_new_patient(new_data):
    """
    Enregistre patient + déclenche fine‑tuning pour DeepSurv uniquement.
    """
    df = load_data()
    new_df = pd.DataFrame([new_data])
    # Enregistrer "OUI"/"NON" pour toutes les colonnes sauf AGE, Tempsdesuivi, Deces
    for c in new_df.columns:
        if c not in ["AGE", "Tempsdesuivi", "Deces"]:
            new_df[c] = new_df[c].apply(lambda x: "OUI" if str(x).upper() == "OUI" else "NON")

    df = pd.concat([df, new_df], ignore_index=True)
    try:
        df.to_excel(DATA_PATH, index=False)
        st.success("Les informations du nouveau patient ont été enregistrées.")
        load_data.clear()
        # Ne faire le fine‑tuning que si c'est un modèle DeepSurv
        update_deepsurv_model()
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement des données : {e}")

def update_deepsurv_model():
    """
    Fine‑tuning du modèle DeepSurv avec l'ensemble des données.
    """
    df = load_data()
    if df.empty:
        st.warning("Base de données vide, pas de mise à jour.")
        return

    X = df[list(FEATURE_CONFIG.keys())].copy()
    for col in X.columns:
        if col != "AGE":
            X[col] = X[col].apply(lambda x: 1.0 if str(x).upper() == "OUI" else 0.0)

    y_event = df["Deces"].apply(lambda x: 1.0 if str(x).upper() == "OUI" else 0.0).values
    y_dur   = df["Tempsdesuivi"].values
    y = np.column_stack([y_event, y_dur])

    model = load_model(MODELS["DeepSurv"])
    if model is None or not isinstance(model, tf.keras.Model):
        return

    model.compile(optimizer=adam, loss=cox_loss)
    st.info("Mise à jour du modèle DeepSurv en cours…")
    model.fit(X, y, epochs=10, batch_size=32)
    model.save(MODELS["DeepSurv"])
    st.success("Modèle DeepSurv mis à jour avec succès.")
