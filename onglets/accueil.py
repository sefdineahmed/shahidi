from PIL import Image
import streamlit as st
import os
from utils import LOGO_PATH  # On récupère ton chemin
import base64

# Fonction pour convertir une image en base64 (obligatoire pour Streamlit)
def get_base64_bg(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

def accueil():
    bg_image = get_base64_bg("assets/background.jpeg")  # Image de fond

    st.markdown(f"""
        <style>
            /* CONTENEUR PRINCIPAL AVEC FOND */
            .custom-bg {{
                background-image: url("{bg_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                height: 80vh; /* 🔁 DIMINUE LA HAUTEUR ICI (ex: 70vh ou 60vh) */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            }}

            /* TITRE PRINCIPAL */
            .main-title {{
                font-size: 20rem;  /* 🔁 AUGMENTE LA TAILLE ICI */
                font-weight: bold;
                color: green;     /* 🔁 COULEUR DU TITRE PRINCIPAL */
                margin-bottom: 6rem;
            }}

            /* SOUS-TITRE */
            .sub-title {{
                font-size: 4rem;  /* 🔁 AUGMENTE OU RÉDUIS ICI */
                color: green;     /* 🔁 COULEUR DU SOUS-TITRE */
                margin-bottom: 2rem;
            }}

            /* BOUTON */
            .custom-btn {{
                padding: 10px 25px;
                font-size: 1.2rem;
                color: white;
                background: linear-gradient(green);
                border: none;
                border-radius: 8px;
                margin-top: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .custom-btn:hover {{
                background: linear-gradient(45deg, #76f2b0, #6e7dff);
            }}
        </style>

        <!-- CONTENU HTML -->
        <div class="custom-bg">
            <h1 class="main-title">L'Innovation Médicale<br>Redéfinie</h1>
            <p class="sub-title">
                Plateforme IA de pointe pour la lutte contre les cancers digestifs
            </p>
            <button class="custom-btn">Découvrir la Technologie</button>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    accueil()

