import streamlit as st
import numpy as np
from datetime import date
import io
from fpdf import FPDF
from utils import (
    FEATURE_CONFIG,
    encode_features,
    load_model,
    predict_survival,
    clean_prediction,
    save_new_patient,
    MODELS,
    TEAM_MEMBERS
)

# Style CSS inchangé...

def generate_pdf_report(input_data, cleaned_pred, model_name):  
    # ... (code identique)  

def show_model_info(selected_model):  
    # ... (code identique)  

def modelisation():
    st.title("📊 Prédiction Intelligente de Survie")

    with st.sidebar:
        st.subheader("⚙️ Configuration")
        selected_model = st.selectbox(
            "Modèle de prédiction",
            options=list(MODELS.keys()),
            format_func=lambda x: f"{x} - {'Deep Learning' if x == 'DeepSurv' else 'Modèle Statistique'}"
        )
        show_model_info(selected_model)

    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📋 Profil Patient")
        inputs = {}
        cols = st.columns(3)
        for i, (feature, label) in enumerate(FEATURE_CONFIG.items()):
            with cols[i % 3]:
                if feature == "AGE":
                    inputs[feature] = st.number_input(label, 18, 120, 50)
                else:
                    inputs[feature] = st.selectbox(label, ["NON", "OUI"])
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔮 Calculer la Prédiction", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            try:
                model = load_model(MODELS[selected_model])
                input_df = encode_features(inputs)
                
                pred = predict_survival(model, input_df)
                cleaned_pred = clean_prediction(pred)

                # Enregistrement
                patient_data = input_df.iloc[0].to_dict()
                patient_data.update({
                    "Tempsdesuivi": cleaned_pred,
                    "Deces": "OUI"
                })
                save_new_patient(patient_data)

                # Affichage
                with st.container():
                    st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric("Survie Estimée", f"{cleaned_pred:.0f} mois")
                    with col2:
                        months = min(int(cleaned_pred), 120)
                        fig = px.line(
                            x=np.arange(months),
                            y=100 * np.exp(-np.log(2) * np.arange(months)/cleaned_pred),
                            labels={"x": "Mois", "y": "Probabilité de Survie (%)"},
                            color_discrete_sequence=['#2e77d0']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # PDF
                    pdf_bytes = generate_pdf_report(inputs, cleaned_pred, selected_model)
                    st.download_button(
                        "📥 Télécharger Rapport",
                        data=pdf_bytes,
                        file_name="rapport_medical.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Erreur : {str(e)}")

if __name__ == "__main__":
    modelisation()
