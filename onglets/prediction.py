import streamlit as st
from utils import (
    FEATURE_CONFIG,
    encode_features,
    load_model,
    predict_survival,
    clean_prediction,
    save_new_patient,
    MODELS
)

def show_prediction():
    st.title("🧠 Prédiction de la survie")
    st.markdown("Renseignez les informations du patient pour estimer le **temps de survie** (en mois).")

    # Formulaire de saisie des données patients
    with st.form("patient_form"):
        age = st.slider("Âge du patient", 18, 100, 50)
        user_inputs = {"AGE": age}

        for key, label in FEATURE_CONFIG.items():
            if key != "AGE":
                response = st.radio(f"{label} ?", ["OUI", "NON"], horizontal=True)
                user_inputs[key] = response

        submitted = st.form_submit_button("🔍 Prédire")

    if submitted:
        st.subheader("📊 Résultat de la prédiction")

        # Encodage des données patient
        data_encoded = encode_features(user_inputs)

        # Chargement du modèle
        model = load_model(MODELS["DeepSurv"])
        if model is None:
            st.error("Erreur de chargement du modèle. Veuillez réessayer plus tard.")
            return

        try:
            # Prédiction
            prediction = predict_survival(model, data_encoded)
            prediction = clean_prediction(prediction)
            st.success(f"✅ Temps de survie estimé : **{prediction:.1f} mois**")

            # Sauvegarde du patient
            save_new_patient(user_inputs)

        except Exception as e:
            st.error(f"❌ Une erreur est survenue lors de la prédiction : {e}")
