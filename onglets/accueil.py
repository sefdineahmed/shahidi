from PIL import Image
import streamlit as st
import os
import base64

# Fonction pour convertir une image en base64
def get_base64_bg(path):
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except:
        return ""

def accueil():
    # Remplace par le bon chemin vers ton image
    bg_image = get_base64_bg("assets/background.jpeg") 

    st.markdown(f"""
        <style>
            /* IMPORTATION DE POLICE */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;400;900&display=swap');

            .main {{
                background-color: #f0f2f6;
            }}

            /* HERO SECTION AVEC OVERLAY */
            .hero-section {{
                background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("{bg_image}");
                background-size: cover;
                background-position: center;
                height: 60vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: white;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin-bottom: 2rem;
            }}

            /* TITRE AVEC EFFET */
            .main-title {{
                font-family: 'Roboto', sans-serif;
                font-size: 4.5vw; /* Taille adaptative très grande */
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 1rem;
                background: linear-gradient(to right, #00f2fe, #4facfe);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
            }}

            .sub-title {{
                font-size: 1.8rem;
                font-weight: 300;
                max-width: 800px;
                line-height: 1.4;
            }}

            /* SECTION CARTES INFO */
            .info-container {{
                display: flex;
                justify-content: space-around;
                gap: 20px;
                margin-top: 2rem;
            }}

            .info-card {{
                background: rgba(255, 255, 255, 0.9);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                flex: 1;
                transition: transform 0.3s ease;
                border-bottom: 5px solid #2e77d0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}

            .info-card:hover {{
                transform: translateY(-10px);
            }}

            .info-card h3 {{
                color: #1e3a8a;
                margin-bottom: 1rem;
            }}

            /* BOUTON MODERNE */
            .stButton>button {{
                background: linear-gradient(45deg, #2e77d0, #4facfe) !important;
                color: white !important;
                border: none !important;
                padding: 15px 40px !important;
                font-size: 1.2rem !important;
                font-weight: bold !important;
                border-radius: 50px !important;
                box-shadow: 0 4px 15px rgba(46, 119, 208, 0.4) !important;
                transition: all 0.3s ease !important;
            }}
            
            .stButton>button:hover {{
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(46, 119, 208, 0.6) !important;
            }}
        </style>

        <div class="hero-section">
            <h1 class="main-title">Innovation Médicale & IA</h1>
            <p class="sub-title">
                Redéfinir la lutte contre les cancers digestifs grâce à l'analyse prédictive et au Deep Learning de pointe.
            </p>
        </div>

        <div style="text-align: center; margin-top: 3rem;">
            <h2 style="color: #0f172a; font-size: 2.5rem;">Pourquoi choisir notre plateforme ?</h2>
        </div>
    """, unsafe_allow_html=True)

    # Utilisation des colonnes Streamlit pour les cartes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="info-card">
                <h3>🚀 Précision</h3>
                <p>Algorithmes de Deep Survival atteignant plus de 92% de C-index.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="info-card">
                <h3>📊 Visualisation</h3>
                <p>Tableaux de bord interactifs pour un suivi patient en temps réel.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="info-card">
                <h3>🔐 Sécurité</h3>
                <p>Protection des données médicales conforme aux standards internationaux.</p>
            </div>
        """, unsafe_allow_html=True)

    # Bouton d'appel à l'action
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Commencer l'analyse →"):
            st.info("Redirection vers l'onglet Analyse...")

if __name__ == "__main__":
    accueil()
