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
    MODELS,
    TEAM_MEMBERS
)

# Style CSS personnalisé  
st.markdown("""  
<style>  
    :root {  
        --primary: #2e77d0;  
        --secondary: #1d5ba6;  
        --accent: #22d3ee;  
    }  
    .st-emotion-cache-1y4p8pa {  
        padding: 2rem 1rem;  
    }  
    .header-card {  
        background: rgba(255, 255, 255, 0.9);  
        border-radius: 15px;  
        padding: 2rem;  
        margin: 1rem 0;  
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);  
    }  
    .prediction-card {  
        background: linear-gradient(135deg, #f8fafc, #ffffff);  
        border-left: 4px solid var(--primary);  
        padding: 1.5rem;  
        margin: 1rem 0;  
    }  
    .model-selector {  
        border-radius: 12px !important;  
        padding: 1rem !important;  
        border: 2px solid var(--primary) !important;  
    }  
    .stButton>button {  
        background: linear-gradient(45deg, var(--primary), var(--secondary)) !important;  
        color: white !important;  
        border-radius: 8px !important;  
        padding: 0.8rem 2rem !important;  
        transition: all 0.3s !important;  
    }  
    .stButton>button:hover {  
        transform: translateY(-2px);  
        box-shadow: 0 4px 15px rgba(46, 119, 208, 0.4) !important;  
    }  
</style>  
""", unsafe_allow_html=True)  


def generate_pdf_report(input_data, cleaned_pred, model_name):  
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
    col_widths = [60, 60]  
    for key, value in input_data.items():  
        pdf.cell(col_widths[0], 8, FEATURE_CONFIG.get(key, key), 1, 0, 'L', 1)  
        pdf.cell(col_widths[1], 8, str(value), 1, 1, 'L')  
  
    pdf.set_font('Arial', 'B', 16)  
    pdf.cell(0, 15, "Résultats de Prédiction", ln=True)  
    pdf.set_font('Arial', '', 14)  
    pdf.cell(0, 8, f"Modèle utilisé : {model_name}", ln=True)  
    pdf.set_text_color(46, 119, 208)  
    pdf.cell(0, 8, f"Survie médiane estimée : {cleaned_pred:.1f} mois", ln=True)  
  
    pdf_buffer = io.BytesIO()  
    pdf.output(pdf_buffer)  
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()  


def show_model_info(selected_model):  
    """Affiche les informations du modèle sélectionné"""  
    model_info = {  
        "DeepSurv": {  
            "description": "Réseau de neurones profond pour l'analyse de survie",  
            "avantages": [  
                "Capture des relations non linéaires",  
                "Adapté aux données complexes",  
                "Mise à jour incrémentale"  
            ]  
        },  
        "CoxPH": {  
            "description": "Modèle de régression de Cox proportionnelle",  
            "avantages": [  
                "Interprétabilité statistique",  
                "Rapide pour les petites données",  
                "Standard en recherche médicale"  
            ]  
        }  
    }  

    with st.sidebar.expander("ℹ️ Info Modèle", expanded=True):  
        st.markdown(f"**{selected_model}**")  
        st.caption(model_info[selected_model]["description"])  
        st.markdown("**Avantages :**")  
        for avantage in model_info[selected_model]["avantages"]:  
            st.markdown(f"- {avantage}")  


def modelisation():  
    st.title("📊 Prédiction Intelligente de Survie")  

    # Sélection du modèle dans la sidebar  
    with st.sidebar:  
        st.subheader("⚙️ Configuration")  
        selected_model = st.selectbox(  
            "Modèle de prédiction",  
            options=list(MODELS.keys()),  
            format_func=lambda x: f"{x} - {'Deep Learning' if x == 'DeepSurv' else 'Modèle Statistique'}",  
            help="Sélectionnez le modèle à utiliser pour la prédiction"  
        )  
        show_model_info(selected_model)  

    # Section de saisie patient  
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
                        options=["NON", "OUI"],  
                        help="Présence de la caractéristique clinique"  
                    )  
        st.markdown("</div>", unsafe_allow_html=True)  

    # Prédiction et résultats  
    if st.button("🔮 Calculer la Prédiction", use_container_width=True):  
        with st.spinner("Analyse en cours..."):  
            try:  
                model = load_model(MODELS[selected_model])  
                input_df = encode_features(inputs)  
                pred = predict_survival(model, input_df)  
                cleaned_pred = clean_prediction(pred)  

                # Enregistrement patient  
                patient_data = input_df.to_dict(orient='records')[0]  
                patient_data["Tempsdesuivi"] = round(cleaned_pred, 1)  
                patient_data["Deces"] = "OUI"  
                save_new_patient(patient_data)  

                # Affichage résultats  
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
                        months = min(int(cleaned_pred), 120)  
                        survival_curve = [100 * np.exp(-np.log(2) * t / cleaned_pred) for t in range(months)]  
                        fig = px.line(  
                            x=list(range(months)),  
                            y=survival_curve,  
                            labels={"x": "Mois", "y": "Probabilité de Survie (%)"},  
                            color_discrete_sequence=['#2e77d0']  
                        )  
                        st.plotly_chart(fig, use_container_width=True)  
                    st.markdown("</div>", unsafe_allow_html=True)  

                    # Génération PDF  
                    pdf_bytes = generate_pdf_report(patient_data, cleaned_pred, selected_model)  
                    st.download_button(  
                        label="📥 Télécharger le Rapport Complet",  
                        data=pdf_bytes,  
                        file_name="rapport_medical.pdf",  
                        mime="application/pdf",  
                        use_container_width=True  
                    )  
            except Exception as e:  
                st.error(f"Erreur de prédiction : {str(e)}")  

    # Section suivi thérapeutique  
    st.markdown("---")  
    with st.expander("📅 Planification du Suivi Thérapeutique", expanded=True):  
        treatment_cols = st.columns(2)  
        with treatment_cols[0]:  
            selected_treatments = st.multiselect(  
                "Options Thérapeutiques",  
                options=["Chimiothérapie", "Exclusive"],  
                help="Sélectionner les traitements à comparer"  
            )  
        with treatment_cols[1]:  
            follow_up_date = st.date_input(  
                "Date de Suivi Recommandée",  
                value=date.today(),  
                help="Date préconisée pour le prochain examen"  
            )  

        if st.button("💾 Enregistrer le Plan de Traitement", use_container_width=True):  
            if selected_treatments:  
                st.toast("Plan de traitement enregistré avec succès !")  
            else:  
                st.warning("Veuillez sélectionner au moins un traitement")  


if __name__ == "__main__":  
    modelisation()
