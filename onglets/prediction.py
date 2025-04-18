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

# --- CSS personnalisé ---
st.markdown("""
<style>
  :root { --primary: #2e77d0; --secondary: #1d5ba6; --accent: #22d3ee; }
  .header-card { background: rgba(255,255,255,0.9); border-radius:15px; padding:2rem; margin:1rem 0; box-shadow:0 4px 20px rgba(0,0,0,0.08); }
  .prediction-card { background: linear-gradient(135deg, #f8fafc, #ffffff); border-left:4px solid var(--primary); padding:1.5rem; margin:1rem 0; }
  .stButton>button { background: linear-gradient(45deg,var(--primary),var(--secondary)) !important; color:white !important; border-radius:8px !important; padding:0.8rem 2rem !important; }
  .stButton>button:hover { transform:translateY(-2px); box-shadow:0 4px 15px rgba(46,119,208,0.4) !important; }
</style>
""", unsafe_allow_html=True)


def generate_pdf_report(input_data, cleaned_pred, model_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',24)
    pdf.set_text_color(46,119,208)
    pdf.cell(0,15,"Rapport Médical SHAHIDI-AI",ln=True,align='C')

    pdf.set_font('Arial','',12)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,10,f"Date : {date.today().strftime('%d/%m/%Y')}",ln=True)

    pdf.set_font('Arial','B',16)
    pdf.cell(0,15,"Paramètres Cliniques",ln=True)
    pdf.set_fill_color(240,248,255)
    pdf.set_font('Arial','',12)
    for key, value in input_data.items():
        pdf.cell(60,8, FEATURE_CONFIG.get(key,key),1,0,'L',1)
        pdf.cell(60,8, str(value),1,1,'L')

    pdf.set_font('Arial','B',16)
    pdf.cell(0,15,"Résultats de Prédiction",ln=True)
    pdf.set_font('Arial','',14)
    pdf.cell(0,8,f"Modèle utilisé : {model_name}",ln=True)
    pdf.set_text_color(46,119,208)
    pdf.cell(0,8,f"Survie médiane estimée : {cleaned_pred:.1f} mois",ln=True)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()


def show_model_info(selected_model):
    model_info = {
        "DeepSurv": {
            "description": "Réseau de neurones profond pour l'analyse de survie",
            "avantages": ["Capture non-linéarités","Données complexes","Fine‑tuning incrémental"]
        },
        "CoxPH": {
            "description": "Régression de Cox proportionnelle",
            "avantages": ["Interprétation statistique","Rapide sur petites données","Norme médicale"]
        }
    }
    with st.sidebar.expander("ℹ️ Info Modèle", expanded=True):
        st.markdown(f"**{selected_model}**")
        st.caption(model_info[selected_model]["description"])
        st.markdown("**Avantages :**")
        for a in model_info[selected_model]["avantages"]:
            st.markdown(f"- {a}")


def modelisation():
    st.title("📊 Prédiction Intelligente de Survie")

    with st.sidebar:
        st.subheader("⚙️ Configuration")
        selected_model = st.selectbox(
            "Modèle de prédiction",
            options=list(MODELS.keys()),
            format_func=lambda x: f"{x} - {'Deep Learning' if x=='DeepSurv' else 'Statistique'}"
        )
        show_model_info(selected_model)

    # Profil patient
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.subheader("📋 Profil Patient")
    inputs = {}
    cols = st.columns(3)
    for i,(feat,label) in enumerate(FEATURE_CONFIG.items()):
        with cols[i%3]:
            if feat=="AGE":
                inputs[feat] = st.number_input(label,18,120,50)
            else:
                inputs[feat] = st.selectbox(label, ["NON","OUI"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Prédiction
    if st.button("🔮 Calculer la Prédiction", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            try:
                model    = load_model(MODELS[selected_model])
                input_df = encode_features(inputs)

                # Debug types
                st.write("Types d'entrée :", input_df.dtypes)

                pred        = predict_survival(model, input_df)
                cleaned_pred = clean_prediction(pred)

                # Sauvegarde
                pdict = input_df.to_dict(orient='records')[0]
                pdict["Tempsdesuivi"] = round(cleaned_pred, 1)
                pdict["Deces"]        = "OUI"
                save_new_patient(pdict)

                # Affichage
                st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)
                c1,c2 = st.columns([1,2])
                with c1:
                    st.metric("Survie Médiane Estimée", f"{cleaned_pred:.0f} mois")
                with c2:
                    months = min(int(cleaned_pred), 120)
                    curve  = [100*np.exp(-np.log(2)*t/cleaned_pred) for t in range(months)]
                    fig = px.line(x=list(range(months)), y=curve,
                                  labels={"x":"Mois","y":"Probabilité de survie (%)"})
                    st.plotly_chart(fig,use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # PDF
                pdfb = generate_pdf_report(pdict, cleaned_pred, selected_model)
                st.download_button("📥 Télécharger le rapport",
                                   data=pdfb, file_name="rapport.pdf",
                                   mime="application/pdf")
            except Exception as e:
                st.error(f"Erreur de prédiction : {e}")

if __name__=="__main__":
    modelisation()
