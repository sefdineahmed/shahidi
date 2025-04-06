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
    predict_survival,
    clean_prediction,
    save_new_patient,
    MODELS
)

# Style CSS personnalisé
st.markdown("""... (identique au code original)""", unsafe_allow_html=True)

def generate_pdf_report(input_data, cleaned_pred, survival_curve_data):
    pdf = FPDF()
    # ... (ajouter la génération de la courbe de survie dans le PDF)
    return pdf_buffer.getvalue()

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
                    inputs[feature] = st.number_input(
                        label, 
                        min_value=18, 
                        max_value=120, 
                        value=50,
                        help="Âge du patient en années"
                    )
                else:
                    inputs[feature] = st.selectbox(
                        label, 
                        options=["Non", "Oui"],
                        help="Présence de la caractéristique clinique"
                    )
        st.markdown("</div>", unsafe_allow_html=True)

    input_df = encode_features(inputs)
    model_name = "DeepSurv"  # Ou sélection dynamique

    if st.button("🔮 Calculer la Prédiction", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            try:
                model = load_model(MODELS[model_name])
                pred = predict_survival(model, input_df)
                cleaned_pred = clean_prediction(pred)

                # Génération de la courbe de survie
                if isinstance(model, CoxPHSurvivalAnalysis):
                    surv_func = model.predict_survival_function(input_df)[0]
                    times = model.event_times_
                    probs = surv_func(times)
                else:
                    risk = model.predict_risk(input_df)[0]
                    baseline_surv = model.baseline_survival_
                    times = baseline_surv.index.values
                    probs = baseline_surv.values ** risk

                with st.container():
                    st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric(
                            label="**Survie Médiane Estimée**", 
                            value=f"{cleaned_pred:.0f} mois",
                            help="Durée médiane de survie prédite"
                        )
                    with col2:
                        fig = px.line(
                            x=times,
                            y=probs*100,
                            labels={"x": "Mois", "y": "Probabilité de Survie (%)"},
                            color_discrete_sequence=['#2e77d0'],
                            title="Courbe de Survie Prédite"
                        )
                        fig.add_hline(y=50, line_dash="dot", line_color="red",
                                    annotation_text="Survie médiane", 
                                    annotation_position="bottom right")
                        fig.update_layout(
                            yaxis_range=[0, 100],
                            xaxis_range=[0, min(times[-1], 120)]
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Sauvegarde et rapport
                patient_data = input_df.to_dict(orient='records')[0]
                save_new_patient(patient_data)
                pdf_bytes = generate_pdf_report(patient_data, cleaned_pred, (times, probs))
                st.download_button(...)

            except Exception as e:
                st.error(f"Erreur de prédiction : {str(e)}")

    # ... (reste du code identique)

if __name__ == "__main__":
    modelisation()
