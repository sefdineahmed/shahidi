import streamlit as st  
import numpy as np  
import plotly.express as px  
from datetime import date  
import io  
from fpdf import FPDF  
from utils import (
    FEATURE_CONFIG,
    encode_features,
    load_model,
    predict_survival_probs,
    calculate_median_survival,
    save_new_patient,
    MODELS,
    BASELINE_SURVIVAL
)

# ... (le CSS reste inchangé)  

def generate_pdf_report(input_data, cleaned_pred, survival_probs):  
    pdf = FPDF()  
    pdf.add_page()  
    # ... (reste inchangé jusqu'aux résultats)  
    pdf.set_text_color(46, 119, 208)  
    pdf.cell(0, 8, f"Survie médiane estimée : {cleaned_pred:.1f} mois", ln=True)  
    
    # Ajout de la courbe de survie
    pdf.image("survival_curve.png", x=10, y=pdf.get_y(), w=180)
    pdf_buffer = io.BytesIO()  
    pdf.output(pdf_buffer)  
    return pdf_buffer.getvalue()  

def modelisation():  
    st.title("📊 Prédiction Intelligente de Survie")  

    with st.container():  
        # ... (saisie des paramètres inchangée)  

    input_df = encode_features(inputs)  
    model_name = "DeepSurv"  
    
    if st.button("🔮 Calculer la Prédiction", use_container_width=True):  
        with st.spinner("Analyse en cours..."):  
            try:  
                model = load_model(MODELS[model_name])  
                # Nouvelle méthode de prédiction
                survival_probs = predict_survival_probs(model, input_df, BASELINE_SURVIVAL)
                median_survival = calculate_median_survival(survival_probs)

                # Enregistrement des données
                patient_data = input_df.to_dict(orient='records')[0]  
                patient_data["Tempsdesuivi"] = round(median_survival, 1)  

                save_new_patient(patient_data)  

                with st.container():  
                    st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)  
                    col1, col2 = st.columns([1, 2])  
                    with col1:  
                        st.metric(
                            label="**Survie Médiane Estimée**", 
                            value=f"{median_survival:.0f} mois" if median_survival < 120 else "60+ mois",  
                            help="Durée médiane de survie prédite"  
                        )  
                    with col2:  
                        # Courbe de survie corrigée
                        time_points = list(survival_probs.keys())
                        prob_values = [survival_probs[t] * 100 for t in time_points]
                        
                        fig = px.line(
                            x=time_points,
                            y=prob_values,
                            labels={"x": "Mois", "y": "Probabilité de Survie (%)"},
                            color_discrete_sequence=['#2e77d0'],
                            title="Courbe de Survie Prédite"
                        )
                        fig.update_layout(yaxis_range=[0, 100])
                        st.plotly_chart(fig, use_container_width=True)
                        
                    st.markdown("</div>", unsafe_allow_html=True)  

                    # Génération PDF
                    pdf_bytes = generate_pdf_report(patient_data, median_survival, survival_probs)  
                    st.download_button(  
                        label="📥 Télécharger le Rapport Complet",  
                        data=pdf_bytes,  
                        file_name="rapport_medical.pdf",  
                        mime="application/pdf",  
                        use_container_width=True  
                    )  
            except Exception as e:  
                st.error(f"Erreur de prédiction : {str(e)}")  

    # ... (le reste reste inchangé)  

if __name__ == "__main__":  
    modelisation()
