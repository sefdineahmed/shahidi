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
    
    .stSelectbox>div>div>select {
        border: 2px solid var(--primary) !important;
        border-radius: 8px !important;
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

    # Section Aperçu des données
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📁 Structure des Données")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df.head(5).style.format(precision=2), height=250)
        with col2:
            st.metric("Nombre de Patients", df.shape[0])
            st.metric("Nombre de Variables", df.shape[1])
            st.metric("Données Manquantes", f"{df.isna().sum().sum()} ({df.isna().mean().mean()*100:.1f}%)")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistiques descriptives
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📈 Statistiques Descriptives")
        
        # Sélecteur de variable
        selected_var = st.selectbox("Sélectionner une Variable", df.columns, key='var_select')
        
        # Cartes de métriques
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h3>Moyenne</h3>
                <p style="font-size:1.5rem; color: var(--primary);">
                    {:.2f}
                </p>
            </div>
            """.format(df[selected_var].mean()), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h3>Médiane</h3>
                <p style="font-size:1.5rem; color: var(--primary);">
                    {:.2f}
                </p>
            </div>
            """.format(df[selected_var].median()), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-card'>
                <h3>Écart-Type</h3>
                <p style="font-size:1.5rem; color: var(--primary);">
                    {:.2f}
                </p>
            </div>
            """.format(df[selected_var].std()), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class='metric-card'>
                <h3>Valeurs Uniques</h3>
                <p style="font-size:1.5rem; color: var(--primary);">
                    {}
                </p>
            </div>
            """.format(df[selected_var].nunique()), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualisations
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("📊 Visualisations Interactives")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Distribution", expanded=True):
                fig = px.histogram(
                    df, 
                    x=selected_var, 
                    nbins=30,
                    color_discrete_sequence=['#2e77d0'],
                    title=f"Distribution de {selected_var}"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            with st.expander("Corrélations", expanded=True):
                numeric_df = df.select_dtypes(include=["number"])
                corr_matrix = numeric_df.corr()
                
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='Blues',
                    zmin=-1,
                    zmax=1
                ))
                fig.update_layout(
                    title='Matrice de Corrélation',
                    height=500,
                    margin=dict(l=50, r=50, b=100, t=100)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analyse des valeurs manquantes
    with st.container():
        st.markdown("<div class='header-card'>", unsafe_allow_html=True)
        st.subheader("🔎 Analyse des Données Manquantes")
        
        missing_data = df.isna().sum().reset_index()
        missing_data.columns = ['Variable', 'Valeurs Manquantes']
        missing_data = missing_data[missing_data['Valeurs Manquantes'] > 0]
        
        if not missing_data.empty:
            fig = px.bar(
                missing_data, 
                x='Variable', 
                y='Valeurs Manquantes',
                color='Valeurs Manquantes',
                color_continuous_scale='Blues',
                title="Répartition des Données Manquantes"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Aucune donnée manquante détectée")
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    analyse_descriptive()
