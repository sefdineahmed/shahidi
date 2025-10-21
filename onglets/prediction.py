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

st.markdown("""
<style>
  :root { --primary: #2e77d0; --secondary: #1d5ba6; }
  .header-card { background:rgba(255,255,255,0.9); border-radius:15px; padding:2rem; margin:1rem 0; }
  .prediction-card { background:linear-gradient(135deg,#f8fafc,#fff); border-left:4px solid var(--primary); padding:1.5rem; margin:1rem 0; }
  .stButton>button { background: linear-gradient(45deg,var(--primary),var(--secondary)) !important; color:white !important; border-radius:8px !important; }
  .stButton>button:hover { box-shadow:0 4px 15px rgba(46,119,208,0.4) !important; }
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
    pdf.cell(0,10,f"Date : {date.today():%d/%m/%Y}",ln=True)
    pdf.set_font('Arial','B',16)
    pdf.cell(0,15,"Paramètres Cliniques",ln=True)
    pdf.set_fill_color(240,248,255)
    pdf.set_font('Arial','',12)
    for k,v in input_data.items():
        pdf.cell(60,8, FEATURE_CONFIG.get(k,k),1,0,'L',1)
        pdf.cell(60,8, str(v),1,1,'L')
    pdf.set_font('Arial','B',16)
    pdf.cell(0,15,"Résultats de Prédiction",ln=True)
    pdf.set_font('Arial','',14)
    pdf.cell(0,8,f"Modèle : {model_name}",ln=True)
    pdf.set_text_color(46,119,208)
    pdf.cell(0,8,f"Survie médiane : {cleaned_pred:.1f} mois",ln=True)
    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf.getvalue()

def show_model_info(selected):
    info = {
        "DeepSurv": {
            "desc": "Réseau de neurones profond pour l'analyse de survie",
            "av": ["Non-linéarités", "Données complexes", "Fine‑tuning incrémental"]
        },
        "CoxPH": {
            "desc": "Régression de Cox proportionnelle",
            "av": ["Statistique interprétable","Rapide","Standard médical"]
        }
    }
    with st.sidebar.expander("Info Modèle", expanded=True):
        st.markdown(f"**{selected}**")
        st.caption(info[selected]["desc"])
        st.markdown("**Avantages :**")
        for a in info[selected]["av"]:
            st.markdown(f"- {a}")

def modelisation():
    st.title("Prédiction Intelligente de Survie")

    with st.sidebar:
        st.subheader("Configuration")
        selected = st.selectbox(
            "Modèle",
            options=list(MODELS.keys()),
            format_func=lambda x: f"{x} - {'Deep Learning' if x=='DeepSurv' else 'Statistique'}"
        )
        show_model_info(selected)

    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.subheader("Profil Patient")
    inputs = {}
    cols = st.columns(3)
    for i,(feat,label) in enumerate(FEATURE_CONFIG.items()):
        with cols[i%3]:
            if feat=="AGE":
                inputs[feat] = st.number_input(label,18,120,50)
            else:
                inputs[feat] = st.selectbox(label,["NON","OUI"])
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Calculer la Prédiction", use_container_width=True):
        with st.spinner("Analyse en cours..."):
            try:
                model = load_model(MODELS[selected])
                df_in = encode_features(inputs)
                st.write("Types :", df_in.dtypes)  # debug
                pred = predict_survival(model, df_in)
                cpred = clean_prediction(pred)

                rec = df_in.to_dict(orient='records')[0]
                rec["Tempsdesuivi"] = round(cpred,1)
                rec["Deces"] = "OUI"
                save_new_patient(rec)

                st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)
                c1,c2 = st.columns([1,2])
                with c1:
                    st.metric("Survie médiane", f"{cpred:.0f} mois")
                with c2:
                    m = min(int(cpred),120)
                    curve = [100*np.exp(-np.log(2)*t/cpred) for t in range(m)]
                    fig = px.line(x=list(range(m)), y=curve,
                                  labels={"x":"Mois","y":"% Survie"})
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                pdfb = generate_pdf_report(rec, cpred, selected)
                st.download_button("Télécharger PDF", pdfb, "rapport.pdf", "application/pdf")
            except Exception as e:
                st.error(f"Erreur de prédiction : {e}")

if __name__=="__main__":
    modelisation()
