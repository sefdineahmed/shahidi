import streamlit as st  
import pandas as pd
import numpy as np  
import plotly.express as px  
from datetime import date  
import io  
import joblib
from fpdf import FPDF  

from utils import (
    FEATURE_CONFIG,
    encode_features,
    load_model,
    predict_survival,
    clean_prediction,
    save_new_patient,
    MODELS
)

# CSS customisé
st.markdown("""  
<style>  
    :root {  
        --primary: #2e77d0;  
        --secondary: #1d5ba6;  
        --accent: #22d3ee;  
    }  
    .header-card { background: rgba(255,255,255,0.9); border-radius: 15px; padding: 2rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }  
    .prediction-card { background: linear-gradient(135deg, #f8fafc, #ffffff); border-left: 4px solid var(--primary); padding: 1.5rem; margin: 1rem 0; }  
    .stButton>button { background: linear-gradient(45deg, var(--primary), var(--secondary)) !important; color: white !important; border-radius: 8px !important; padding: 0.8rem 2rem !important; transition: all 0.3s !important; }  
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(46, 119, 208, 0.4) !important; }  
</style>  
""", unsafe_allow_html=True)

def generate_pdf_report(input_data, cleaned_pred):  
    pdf = FPDF()  
    pdf.add_page()  
    pdf.set_font('Arial', 'B', 24)  
    pdf.set_text_color(46, 119, 208)  
    pdf.cell(0, 15, "Rapport Médical SHAHIDI-AI", ln=True, align='C')  
  
    pdf.set_font('Arial', '', 12)  
    pdf.set_text_color(0, 0, 0)  
    pdf.cell(0, 10, f"Date : {date.today().strftime('%d/%m/%Y')}", ln=True)  
  
    pdf.set_font('Arial', 'B', 16)  
    pdf.cell(0, 15, "Paramètres Cliniques", ln=True)  
    pdf.set_fill_color(240, 248, 255)  
  
    pdf.set_font('Arial', '', 12)  
    for key, value in input_data.items():  
        if key not in ["Tempsdesuivi", "Deces"]:  
            pdf.cell(60, 8, FEATURE_CONFIG.get(key, key), 1, 0, 'L', 1)  
            pdf.cell(60, 8, str(value), 1, 1, 'L')  
  
    pdf.set_font('Arial', 'B', 16)  
    pdf.cell(0, 15, "Résultats de Prédiction", ln=True)  
    pdf.set_font('Arial', '', 14)  
    pdf.cell(0, 8, "Modèle utilisé : DeepSurv", ln=True)  
    pdf.set_text_color(46, 119, 208)  
    pdf.cell(0, 8, f"Survie médiane estimée : {cleaned_pred:.1f} mois", ln=True)  
  
    pdf_buffer = io.BytesIO()  
    pdf.output(pdf_buffer)  
    return pdf_buffer.getvalue()  

def load_calibration():
    try:
        cal = joblib.load("models/calibration.pkl")
        return cal.get("thresholds", None), cal.get("medians", None)
    except Exception:
        return None, None

def modelisation():  
    st.title("📊 Prédiction Intelligente de Survie")  
  
    with st.container():  
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)  
        st.subheader("📋 Profil Patient")  
        inputs = {}  
        cols = st.columns(3)  
        for i, (feature, label) in enumerate(FEATURE_CONFIG.items()):  
            with cols[i % 3]:  
                if feature == "AGE":  
                    inputs[feature] = st.number_input(label, min_value=18, max_value=120, value=50)  
                else:  
                    inputs[feature] = st.selectbox(label, options=["NON", "OUI"])  
        st.markdown("</div>", unsafe_allow_html=True)  

    input_df = encode_features(inputs)
    input_df = input_df.apply(pd.to_numeric, errors='coerce')

    model_name = "DeepSurv"  

    if st.button("🔮 Calculer la Prédiction", use_container_width=True):  
        with st.spinner("Analyse en cours..."):  
            try:  
                model = load_model(MODELS[model_name])
                thresholds, medians = load_calibration()
                pred = predict_survival(model, input_df, thresholds, medians)
                cleaned_pred = clean_prediction(pred)

                patient_data = inputs.copy()  
                patient_data["Tempsdesuivi"] = round(cleaned_pred, 1)  
                patient_data["Deces"] = "OUI"  

                save_new_patient(patient_data)

                st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)  
                col1, col2 = st.columns([1, 2])  
                with col1:  
                    st.metric("**Survie Médiane Estimée**", f"{cleaned_pred:.0f} mois")

                    # Affichage du groupe de risque estimé
                    if thresholds:
                        risk_score = float(model.predict(input_df).flatten()[0])
                        group = sum(risk_score > t for t in thresholds)
                        group_label = ["🟢 Faible", "🟠 Moyen", "🔴 Élevé"][min(group, 2)]
                        st.info(f"**Groupe de Risque Estimé** : {group_label}")

                with col2:  
                    months = min(int(cleaned_pred), 120)  
                    survival_curve = [100 * np.exp(-np.log(2) * t / cleaned_pred) for t in range(months)]  
                    fig = px.line(x=list(range(months)), y=survival_curve, labels={"x": "Mois", "y": "Probabilité de Survie (%)"}, color_discrete_sequence=['#2e77d0'])  
                    st.plotly_chart(fig, use_container_width=True)  

                st.markdown("</div>", unsafe_allow_html=True)  

                pdf_bytes = generate_pdf_report(patient_data, cleaned_pred)  
                st.download_button("📥 Télécharger le Rapport Complet", data=pdf_bytes, file_name="rapport_medical.pdf", mime="application/pdf", use_container_width=True)  

            except Exception as e:  
                st.error(f"Erreur de prédiction : {str(e)}")  

    st.markdown("---")  
    with st.expander("📅 Planification du Suivi Thérapeutique", expanded=True):  
        cols = st.columns(2)  
        with cols[0]:  
            selected_treatments = st.multiselect("Options Thérapeutiques", options=["Chimiothérapie", "Exclusive"])  
        with cols[1]:  
            follow_up_date = st.date_input("Date de Suivi Recommandée", value=date.today())  

        if st.button("💾 Enregistrer le Plan de Traitement", use_container_width=True):  
            if selected_treatments:  
                st.toast("Plan de traitement enregistré avec succès !")  
            else:  
                st.warning("Veuillez sélectionner au moins un traitement")  

if __name__ == "__main__":  
    modelisation()
