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
                color: red;     /* 🔁 COULEUR DU TITRE PRINCIPAL */
                margin-bottom: 6rem;
                animation: fadeInTitle 3s ease-in-out;
            }}

            /* SOUS-TITRE */
            .sub-title {{
                font-size: 4rem;  /* 🔁 AUGMENTE OU RÉDUIS ICI */
                color: red;     /* 🔁 COULEUR DU SOUS-TITRE */
                margin-bottom: 2rem;
                animation: fadeInSubTitle 4s ease-in-out;
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
                animation: fadeInButton 5s ease-in-out;
            }}
            .custom-btn:hover {{
                background: linear-gradient(45deg, #76f2b0, #6e7dff);
            }}

            /* ANIMATION FADE IN */
            @keyframes fadeInTitle {{
                0% {{ opacity: 0; transform: translateY(-50px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes fadeInSubTitle {{
                0% {{ opacity: 0; transform: translateY(50px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes fadeInButton {{
                0% {{ opacity: 0; transform: scale(0.8); }}
                100% {{ opacity: 1; transform: scale(1); }}
            }}

            /* SECTION SUPPLÉMENTAIRE */
            .impression-section {{
                background-color: #F0F4F8;
                padding: 3rem 0;
                text-align: center;
                animation: slideInUp 2s ease-in-out;
            }}
            .impression-section h2 {{
                font-size: 3rem;
                color: #1e3a8a;
                margin-bottom: 2rem;
            }}
            .impression-section p {{
                font-size: 1.5rem;
                color: #334155;
                margin-bottom: 2rem;
            }}
            .impression-section .highlight-btn {{
                padding: 12px 30px;
                font-size: 1.3rem;
                color: white;
                background: #2e77d0;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .impression-section .highlight-btn:hover {{
                background: #1a5fa4;
            }}
            @keyframes slideInUp {{
                0% {{ opacity: 0; transform: translateY(50px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}

            /* CARROUSEL D'IMAGES */
            .carousel-section {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 4rem;
                padding: 3rem 0;
                animation: fadeInCarousel 3s ease-in-out;
            }}
            .carousel-img {{
                width: 25rem;
                height: 25rem;
                margin: 0 2rem;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }}
            .carousel-img:hover {{
                transform: scale(1.1);
            }}
            @keyframes fadeInCarousel {{
                0% {{ opacity: 0; transform: translateY(50px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>

        <!-- CONTENU HTML -->
        <div class="custom-bg">
            <h1 class="main-title"> Bienvenue dans notre Plateforme d'innovation Médicale </h1>
            <p class="sub-title">
                Plateforme IA de pointe pour la lutte contre les cancers digestifs
            </p>
            <button class="custom-btn">Découvrir la Technologie</button>
        </div>

        <!-- SECTION IMPRESSIONNANTE -->
        <div class="impression-section">
            <h2>Un Futur Prometteur avec l'IA</h2>
            <p>Notre plateforme révolutionne l'approche diagnostique et thérapeutique des cancers digestifs, en vous offrant des prédictions de survie précises et des solutions innovantes basées sur l'intelligence artificielle.</p>
            <button class="highlight-btn">Explorez Notre Solution</button>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    accueil()
