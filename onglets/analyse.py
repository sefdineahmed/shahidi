import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data  # Assurez-vous que cette fonction existe

# Style CSS personnalisé
st.markdown("""
<style>
    :root {
        --primary: #2e77d0;
        --secondary: #1d5ba6;
        --accent: #22d3ee;
    }

    .header-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid var(--primary);
    }

    .metric-card {
        background: linear-gradient(135deg, #f8faff, #ffffff);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }

    .metric-card:hover {
        transform: translateY(-3px);
    }

    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def analyse_descriptive():
    st.title("🔍 Analyse Exploratoire des Données")

    # Chargement des données
    df = load_data()
    if df.empty:
        st.error("Aucune donnée disponible")
        return

    # SECTION 1 - STRUCTURE DES DONNÉES
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📁 Structure des Données")

        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de Patients", df.shape[0])
        col2.metric("Nombre de Variables", df.shape[1])
        col3.metric("Données Manquantes", f"{df.isna().sum().sum()} ({df.isna().mean().mean()*100:.1f}%)")

        st.dataframe(df.head(5).style.format(precision=2), height=250)
        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 2 - VARIABLES CATÉGORIELLES
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("🏷️ Variables Catégorielles")

        cat_vars = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        if cat_vars:
            st.write("Variables catégorielles détectées :")
            st.code(", ".join(cat_vars), language='text')
        else:
            st.info("Aucune variable catégorielle détectée.")
        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 3 - STATISTIQUES DESCRIPTIVES
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📈 Statistiques Descriptives")

        selected_var = st.selectbox("Sélectionner une variable à analyser :", df.columns)

        # Si la variable est numérique
        if pd.api.types.is_numeric_dtype(df[selected_var]):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Moyenne", f"{df[selected_var].mean():.2f}")
            col2.metric("Médiane", f"{df[selected_var].median():.2f}")
            col3.metric("Écart-type", f"{df[selected_var].std():.2f}")
            col4.metric("Valeurs uniques", df[selected_var].nunique())

        # Sinon (catégorielle)
        else:
            mode = df[selected_var].mode().iloc[0]
            count_mode = df[selected_var].value_counts().iloc[0]
            n_unique = df[selected_var].nunique()
            col1, col2, col3 = st.columns(3)
            col1.metric("Valeur la plus fréquente", mode)
            col2.metric("Effectif", count_mode)
            col3.metric("Valeurs uniques", n_unique)

        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 4 - VISUALISATIONS
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📊 Visualisations")

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Distribution", expanded=True):
                if pd.api.types.is_numeric_dtype(df[selected_var]):
                    fig = px.histogram(df, x=selected_var, nbins=30, color_discrete_sequence=['#2e77d0'])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = px.bar(df[selected_var].value_counts().reset_index(),
                                 x='index', y=selected_var,
                                 color_discrete_sequence=['#2e77d0'],
                                 labels={'index': selected_var, selected_var: 'Effectif'})
                    st.plotly_chart(fig, use_container_width=True)

        with col2:
            with st.expander("Corrélations (numériques uniquement)", expanded=True):
                numeric_df = df.select_dtypes(include=["number"])
                if numeric_df.shape[1] >= 2:
                    corr_matrix = numeric_df.corr()
                    fig = go.Figure(data=go.Heatmap(
                        z=corr_matrix,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale='Blues',
                        zmin=-1, zmax=1
                    ))
                    fig.update_layout(title='Matrice de Corrélation', height=500)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pas assez de variables numériques pour afficher une matrice de corrélation.")

        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 5 - DONNÉES MANQUANTES
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("🔎 Données Manquantes")

        missing_data = df.isna().sum().reset_index()
        missing_data.columns = ['Variable', 'Valeurs Manquantes']
        missing_data = missing_data[missing_data['Valeurs Manquantes'] > 0]

        if not missing_data.empty:
            fig = px.bar(
                missing_data,
                x='Variable',
                y='Valeurs Manquantes',
                color='Valeurs Manquantes',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Aucune donnée manquante détectée.")

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    analyse_descriptive()
