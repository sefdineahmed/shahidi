import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data  # Assurez-vous que cette fonction existe

# CSS personnalisé
st.markdown("""
<style>
    .header-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #2e77d0;
    }
    .metric-box {
        background-color: #f2f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2rem;
        color: #2e77d0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def analyse_descriptive():
    st.title("Analyse Exploratoire des Données")

    df = load_data()
    if df.empty:
        st.error("Aucune donnée disponible")
        return

    # ────────── Aperçu ──────────
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.subheader("Vue d'Ensemble")
    st.dataframe(df.head(), height=250)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='metric-box'>Nombre de Patients<br><span class='metric-value'>{}</span></div>".format(df.shape[0]), unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric-box'>Nombre de Variables<br><span class='metric-value'>{}</span></div>".format(df.shape[1]), unsafe_allow_html=True)
    with c3:
        missing = df.isna().sum().sum()
        missing_pct = df.isna().mean().mean() * 100
        st.markdown("<div class='metric-box'>Données Manquantes<br><span class='metric-value'>{} ({:.1f}%)</span></div>".format(missing, missing_pct), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ────────── Statistiques descriptives ──────────
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.subheader("Statistiques Descriptives")

    selected_var = st.selectbox("Sélectionner une variable à analyser", df.columns)

    if pd.api.types.is_numeric_dtype(df[selected_var]):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Moyenne", f"{df[selected_var].mean():.2f}")
        with col2:
            st.metric("Médiane", f"{df[selected_var].median():.2f}")
        with col3:
            st.metric("Écart-Type", f"{df[selected_var].std():.2f}")
        with col4:
            st.metric("Valeurs Uniques", f"{df[selected_var].nunique()}")

        fig = px.histogram(df, x=selected_var, nbins=30, color_discrete_sequence=['#2e77d0'])
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(f"Variable catégorielle détectée : **{selected_var}**")
        cat_counts = df[selected_var].value_counts().reset_index()
        cat_counts.columns = [selected_var, "Effectif"]

        fig = px.bar(cat_counts, x=selected_var, y="Effectif", color="Effectif", color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(cat_counts)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    # ────────── Corrélation ──────────
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.subheader("Matrice de Corrélation")

    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        corr = numeric_df.corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr,
            x=corr.columns,
            y=corr.columns,
            colorscale='Blues',
            zmin=-1,
            zmax=1
        ))
        fig.update_layout(title="Corrélation entre variables numériques", height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aucune variable numérique pour la corrélation")
    st.markdown("</div>", unsafe_allow_html=True)

    # ────────── Valeurs manquantes ──────────
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.subheader("Analyse des Données Manquantes")

    missing_data = df.isna().sum()
    missing_data = missing_data[missing_data > 0].reset_index()
    missing_data.columns = ["Variable", "Valeurs Manquantes"]

    if not missing_data.empty:
        fig = px.bar(missing_data, x="Variable", y="Valeurs Manquantes", color="Valeurs Manquantes", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("Aucune donnée manquante détectée")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    analyse_descriptive()
