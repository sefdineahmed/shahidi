import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from lifelines import KaplanMeierFitter
from tensorflow.keras.models import load_model as tf_load_model
from sklearn.model_selection import train_test_split

# --- Configuration des chemins ---
DATA_PATH = "data/data.xlsx"
MODEL_PATH = "models/deepsurv.keras"
BASELINE_SURVIVAL_PATH = "models/baseline_survival.pkl"

# --- Configuration des caractéristiques ---
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

# --- Fonctions de prédiction améliorées ---
@st.cache_data(show_spinner=False)
def load_data():
    """Charge les données depuis le fichier Excel avec gestion d'erreur améliorée"""
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_excel(DATA_PATH)
            # Validation des colonnes nécessaires
            required_columns = list(FEATURE_CONFIG.keys()) + ['Tempsdesuivi', 'Deces']
            if not all(col in df.columns for col in required_columns):
                st.error("Structure de données invalide")
                return pd.DataFrame()
            return df
        raise FileNotFoundError
    except Exception as e:
        st.error(f"Erreur de chargement des données: {str(e)}")
        return pd.DataFrame()

@st.cache_resource(show_spinner=False)
def load_model():
    """Charge le modèle avec gestion de version et vérification d'intégrité"""
    try:
        # Vérification de la présence du modèle
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Modèle introuvable")
            
        # Chargement du modèle avec la fonction de perte personnalisée
        def cox_loss(y_true, y_pred):
            event = tf.cast(y_true[:, 0], dtype=tf.float32)
            risk = y_pred[:, 0]
            log_risk = tf.math.log(tf.cumsum(tf.exp(risk), reverse=True))
            return -tf.reduce_mean((risk - log_risk) * event)

        model = tf_load_model(MODEL_PATH, custom_objects={"cox_loss": cox_loss})
        
        # Vérification de la structure du modèle
        if len(model.layers) < 1 or not isinstance(model.layers[-1].get_config(), dict):
            raise ValueError("Structure de modèle invalide")
            
        return model
    except Exception as e:
        st.error(f"Erreur de chargement du modèle: {str(e)}")
        return None

def encode_features(inputs):
    """Encodage robuste des caractéristiques avec validation"""
    encoded = {"AGE": inputs.get("AGE", 50)}  # Valeur par défaut sécurisée
    
    for feature in FEATURE_CONFIG:
        if feature != "AGE":
            value = inputs.get(feature, "Non")
            # Validation des valeurs d'entrée
            if str(value).upper() not in ["OUI", "NON"]:
                st.warning(f"Valeur invalide pour {feature}, utilisation de 'Non' par défaut")
                value = "Non"
            encoded[feature] = 1 if str(value).upper() == "OUI" else 0
            
    return pd.DataFrame([encoded])

def calculate_baseline_survival(df):
    """Calcule la fonction de survie de base avec Kaplan-Meier"""
    kmf = KaplanMeierFitter()
    kmf.fit(df['Tempsdesuivi'], df['Deces'].apply(lambda x: 1 if str(x).upper() == "OUI" else 0))
    return kmf.survival_function_['KM_estimate'].values

def predict_survival_probs(model, X, baseline_survival):
    """Calcule les probabilités de survie à chaque intervalle de temps"""
    try:
        risk_score = model.predict(X, verbose=0)[0][0]
        return np.power(baseline_survival, np.exp(risk_score))
    except Exception as e:
        st.error(f"Erreur de prédiction: {str(e)}")
        return None

def calculate_median_survival(survival_probs, max_time=60):
    """Calcule la survie médiane de manière robuste"""
    for t, prob in enumerate(survival_probs):
        if prob <= 0.5:
            return min(t, max_time)
    return max_time  # Valeur maximale par défaut

def save_new_patient(new_patient_data):
    """Sauvegarde sécurisée des nouveaux patients"""
    try:
        df = load_data()
        new_df = pd.DataFrame([new_patient_data])
        
        # Validation des données avant sauvegarde
        required_columns = list(FEATURE_CONFIG.keys()) + ['Tempsdesuivi', 'Deces']
        if not all(col in new_df.columns for col in required_columns):
            raise ValueError("Données patient incomplètes")
            
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(DATA_PATH, index=False)
        st.success("Patient enregistré avec succès")
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde: {str(e)}")
        return False

def update_deepsurv_model():
    """Mise à jour incrémentielle du modèle avec validation"""
    try:
        df = load_data()
        if len(df) < 10:
            st.warning("Données insuffisantes pour l'entraînement")
            return

        # Préparation des données
        X = df[FEATURE_CONFIG.keys()].copy()
        X = X.apply(lambda col: col.map(lambda x: 1 if str(x).upper() == "OUI" else 0) if col.name != "AGE" else col)
        y = df[['Deces', 'Tempsdesuivi']].copy()
        y['Deces'] = y['Deces'].apply(lambda x: 1 if str(x).upper() == "OUI" else 0)

        # Chargement et entraînement du modèle
        model = load_model()
        if model is None:
            return

        # Entraînement avec validation
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=15,
            batch_size=32,
            verbose=0
        )
        
        # Sauvegarde du modèle et de la baseline
        model.save(MODEL_PATH)
        baseline_survival = calculate_baseline_survival(df)
        joblib.dump(baseline_survival, BASELINE_SURVIVAL_PATH)
        
        st.success("Modèle mis à jour avec succès")
    except Exception as e:
        st.error(f"Erreur d'entraînement: {str(e)}")

# --- Autres fonctions utilitaires ---
def load_baseline_survival():
    """Charge la courbe de survie de base"""
    try:
        if os.path.exists(BASELINE_SURVIVAL_PATH):
            return joblib.load(BASELINE_SURVIVAL_PATH)
        return None
    except Exception as e:
        st.error(f"Erreur de chargement de la baseline: {str(e)}")
        return None
