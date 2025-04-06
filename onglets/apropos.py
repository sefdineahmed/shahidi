from PIL import Image
import streamlit as st
import os
import base64
from utils import LOGO_PATH TEAM_MEMBERS # On récupère le chemin défini dans utils.py

# Fonction pour convertir une image en base64 (utile pour le background)
def get_base64_bg(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

def a_propos():
    # Convertir l'image du logo en base64 pour l'utiliser comme background
    bg_image = get_base64_bg(LOGO_PATH)

    # Section HERO avec le style inspiré de "accueil"
    st.markdown(f"""
        <style>
            .custom-bg {{
                background-image: url("{bg_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                height: 80vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
            }}

            .main-title {{
                font-size: 3rem;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 1rem;
            }}

            .sub-title {{
                font-size: 1.5rem;
                color: #ffffff;
            }}
        </style>

        <div class="custom-bg">
            <h1 class="main-title">🩺 Prévision du Temps de Survie du Cancer Gastrique</h1>
            <p class="sub-title">L'intelligence artificielle au service de l'oncologie clinique au Sénégal.</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------------------------
    # Section Statistiques Clés
    st.markdown("### Principaux Indicateurs Épidémiologiques")
    cols = st.columns(3)
    stats = [
        {"icon": "🕒", "value": "58%", "label": "Survie à 5 ans"},
        {"icon": "📈", "value": "1200+", "label": "Cas annuels"},
        {"icon": "🎯", "value": "89%", "label": "Précision du modèle"}
    ]
    for col, stat in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{stat['icon']}</div>
                <div style="font-size: 2.2rem; font-weight: 700; color: #0f172a;">
                    {stat['value']}
                </div>
                <div style="color: #334155; font-size: 1rem;">
                    {stat['label']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Section Performance des Modèles
    st.markdown("## Performance des Modèles", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 10px;">
        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
            <thead>
                <tr>
                    <th style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">Modèle</th>
                    <th style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">C-index</th>
                    <th style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">IBS</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">Random Survival Forest</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.84</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.077</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">Cox PH</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.85</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.080</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">Gradient Boosting</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.87</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.085</td>
                </tr>
                <tr style="background-color: #d1fae5; font-weight: bold;">
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">Deep Survival</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.92</td>
                    <td style="border: 1px solid #ccc; padding: 0.75rem; text-align: center;">0.044</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Section Analyse des Performances
    st.markdown("## Analyse des Performances", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            st.markdown(
                """
                <style>
                    .image-container img {
                        height: 10px;  /* Ajuste la hauteur de l'image ici */
                        object-fit: contain; /* Maintient l'aspect ratio de l'image */
                    }
                </style>
                """, unsafe_allow_html=True
            )
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image("assets/ibs_curve.jpeg", caption="Courbe IBS - Comparaison des modèles", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erreur de chargement de l'image : {str(e)}")

    with col2:
        st.markdown("""
        <div style="background: rgba(white); padding: 1rem; border-radius: 10px;">
            <h3>Interprétation des Résultats</h3>
            <ul style="line-height: 1.8;">
                <li>📉 Meilleure performance du modèle Deep Survival</li>
                <li>⏱ Stabilité temporelle des prédictions</li>
                <li>🎯 Faible erreur intégrée (IBS)</li>
            </ul>
            <div style="background-color: #2e77d0; color: #fff; padding: 6px 12px; border-radius: 20px; display: inline-block; margin-top: 10px; font-size: 0.85rem;">
                🔬 Validation croisée (k=10)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Section Équipe de Recherche
    st.markdown("## Équipe de Recherche", unsafe_allow_html=True)
    cols = st.columns(3)
    team_members = [
        {"photo": "assets/team/aba.jpeg", "name": "Pr. Aba Diop", "role": "Épidémiologiste"},
        {"photo": "assets/team/sy.jpeg", "name": "Dr. Idrissa Sy", "role": "Data Scientist"},
        {"photo": "assets/team/sefdine.jpeg", "name": "Ahmed Sefdine", "role": "Ingénieur Biomédical"}
    ]
    
    for col, member in zip(cols, team_members):
        with col:
            try:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.8); text-align: center; padding: 1rem; border-radius: 10px; margin-top: 1rem; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                    <img src="{member['photo']}" style="width: 100%; border-radius: 10px; height: 220px; object-fit: cover; border: 3px solid #2e77d0;" alt="{member['name']}">
                    <h3 style="margin: 0.5rem 0; color: #0f172a;">{member['name']}</h3>
                    <p style="margin: 0; color: #334155;">{member['role']}</p>
                    <div style="background-color: #2e77d0; color: #fff; padding: 6px 12px; border-radius: 20px; display: inline-block; margin-top: 10px; font-size: 0.85rem;">
                        🏥 CHU Dakar
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur d'affichage du profil : {str(e)}")

if __name__ == "__main__":
    a_propos()
