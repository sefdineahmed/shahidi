# prediction.py

import streamlit as st
import numpy as np
from utils import (
    MODELS, FEATURE_CONFIG, load_data,
    load_deepsurv_model, load_cox_model,
    encode_features, calibrate_median_survival_by_risk_group,
    predict_survival, clean_prediction, save_new_patient
)

def main():
    st.set_page_config(page_title="Prédiction survie", layout="centered")
    st.sidebar.title("Sélection du modèle")
    model_name = st.sidebar.selectbox("Modèle", list(MODELS.keys()))
    model_path = MODELS[model_name]

    # Chargement du modèle choisi
    if model_name == "DeepSurv":
        model = load_deepsurv_model(model_path)
    else:
        model = load_cox_model(model_path)
    if model is None:
        st.stop()

    st.title("🩺 Prédiction du temps de survie")
    st.write("Renseignez les caractéristiques du patient :")

    # Saisie des caractéristiques
    inputs = {}
    for key, label in FEATURE_CONFIG.items():
        if key == "AGE":
            inputs[key] = st.number_input(label, min_value=0, max_value=120, value=50)
        else:
            inputs[key] = st.selectbox(label, ["Non", "Oui"], index=0)

    # Bouton de prédiction
    if st.button("🔍 Prédire"):
        data_df = encode_features(inputs)

        # Calibration à partir des données existantes
        df = load_data()
        features = list(FEATURE_CONFIG.keys())
        X_train = df[features].copy()
        for col in features:
            if col != "AGE":
                X_train[col] = X_train[col].apply(lambda x: 1 if str(x).upper() == "OUI" else 0)
        y_time = df["Tempsdesuivi"].astype(float).values
        y_event = df["Deces"].apply(lambda x: 1 if str(x).upper() == "OUI" else 0).values
        y_train = np.column_stack([y_event, y_time])

        thresholds, medians = calibrate_median_survival_by_risk_group(model, X_train, y_train)
        raw_pred = predict_survival(model, data_df, thresholds, medians)
        pred = clean_prediction(raw_pred)

        st.success(f"🔮 Temps de survie estimé : **{pred:.1f}** mois")

        # Option d'enregistrement
        if st.checkbox("Enregistrer ce patient avec la prévision"):
            new_pat = {**inputs, "Tempsdesuivi": pred, "Deces": "Non"}
            try:
                save_new_patient(new_pat)
                st.info("✅ Patient ajouté à la base.")
            except Exception as e:
                st.error(f"Erreur sauvegarde : {e}")

if __name__ == "__main__":
    main()
