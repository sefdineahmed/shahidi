import streamlit as st
import os
import base64
from utils import LOGO_PATH, TEAM_MEMBERS  # On récupère le chemin du fond et la liste des membres

# Fonction pour convertir une image en base64 (obligatoire pour Streamlit)
def get_base64_bg(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

def a_propos():
    bg_image = get_base64_bg(LOGO_PATH)
    # CSS personnalisé intégrant le style du fond et les profils d'équipe
    st.markdown(f"""
        <style>
            /* Fond de page personnalisé */
            body {{
                background-image: url("{bg_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            /* Superposition pour une meilleure lisibilité */
            .overlay {{
                background: rgba(0, 0, 0, 0.6);
                padding: 2rem;
                border-radius: 10px;
                margin: 2rem 0;
            }}
            /* Titres */
            h1, h2, h3 {{
                color: #ffffff;
                text-align: center;
            }}
            /* Paragraphe */
            p, li {{
                color: #d1d5db;
            }}
            /* Cartes de statistiques et performance */
            .data-card {{
                background: rgba(255, 255, 255, 0.2);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 1rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            /* Tableau de performance */
            .performance-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 1rem;
            }}
            .performance-table th, .performance-table td {{
                border: 1px solid rgba(255,255,255,0.3);
                padding: 0.75rem;
                text-align: center;
            }}
            .performance-table th {{
                background-color: rgba(255,255,255,0.2);
            }}
            .highlight {{
                background-color: rgba(46, 119, 208, 0.6);
                font-weight: bold;
            }}
            /* Profil équipe */
            .team-card {{
                background: rgba(255, 255, 255, 0.2);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin: 1rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            .team-photo {{
                width: 100%;
                height: 220px;
                border-radius: 10px;
                object-fit: cover;
                border: 3px solid #2e77d0;
                margin-bottom: 0.5rem;
            }}
            .metric-badge {{
                background-color: #2e77d0;
                color: #fff;
                padding: 6px 12px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 10px;
                font-size: 0.85rem;
            }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        # Section Héro
        st.markdown("""
            <div class="overlay">
                <h1>🩺 Prévision du Temps de Survie du Cancer Gastrique</h1>
                <p style="font-size:1.2rem;">
                    L'intelligence artificielle au service de l'oncologie clinique au Sénégal.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Section Statistiques Clés
        st.markdown("<div class='overlay'><h2>Principaux Indicateurs Épidémiologiques</h2></div>", unsafe_allow_html=True)
        cols = st.columns(3)
        stats = [
            {"icon": "🕒", "value": "58%", "label": "Survie à 5 ans"},
            {"icon": "📈", "value": "1200+", "label": "Cas annuels"},
            {"icon": "🎯", "value": "89%", "label": "Précision du modèle"}
        ]
        for col, stat in zip(cols, stats):
            with col:
                st.markdown(f"""
                <div class="data-card">
                    <div style="font-size: 2.5rem;">{stat['icon']}</div>
                    <div style="font-size: 2.2rem; font-weight: 700;">{stat['value']}</div>
                    <div style="font-size: 1rem;">{stat['label']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Section Performance des Modèles
        st.markdown("<div class='overlay'><h2>Performance des Modèles</h2></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="data-card">
            <table class="performance-table">
                <thead>
                    <tr>
                        <th>Modèle</th>
                        <th>C-index</th>
                        <th>IBS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Random Survival Forest</td>
                        <td>0.84</td>
                        <td>0.077</td>
                    </tr>
                    <tr>
                        <td>Cox PH</td>
                        <td>0.85</td>
                        <td>0.080</td>
                    </tr>
                    <tr>
                        <td>Gradient Boosting</td>
                        <td>0.87</td>
                        <td>0.085</td>
                    </tr>
                    <tr class="highlight">
                        <td>Deep Survival</td>
                        <td>0.92</td>
                        <td>0.044</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Section Analyse des Performances
        st.markdown("<div class='overlay'><h2>Analyse des Performances</h2></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            try:
                st.image("assets/ibs_curve.jpeg", caption="Courbe IBS - Comparaison des modèles", use_container_width=True)
            except Exception as e:
                st.error(f"Erreur de chargement de l'image : {str(e)}")
        with col2:
            st.markdown("""
                <div class="data-card">
                    <h3>Interprétation des Résultats</h3>
                    <ul style="line-height: 1.8;">
                        <li>📉 Meilleure performance du modèle Deep Survival</li>
                        <li>⏱ Stabilité temporelle des prédictions</li>
                        <li>🎯 Faible erreur intégrée (IBS)</li>
                    </ul>
                    <div class="metric-badge">🔬 Validation croisée (k=10)</div>
                </div>
            """, unsafe_allow_html=True)

        # Section Équipe Scientifique
        st.markdown("<div class='overlay'><h2>Équipe de Recherche</h2></div>", unsafe_allow_html=True)
        cols = st.columns(3)
        # On parcourt TEAM_MEMBERS (défini dans utils.py) pour afficher les profils
        for member in TEAM_MEMBERS:
            with cols.pop(0) if cols else st.columns(3)[0]:
                st.markdown(f"""
                    <div class="team-card">
                        <img src="{member['photo']}" class="team-photo" alt="{member['name']}">
                        <h3>{member['name']}</h3>
                        <p>{member['role']}</p>
                        <div>
                            <span class="metric-badge">{member.get('Etablissement', 'CHU Dakar')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        # Réorganisation des colonnes si le nombre de membres dépasse celui de la première rangée
        # Vous pouvez également ajuster la mise en page en fonction du nombre de membres.
        
if __name__ == "__main__":
    a_propos()
