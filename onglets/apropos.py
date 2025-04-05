from PIL import Image
import streamlit as st
import os
import pandas as pd

LOGO_PATH = "assets/background.jpeg"  # Chemin de l'image de fond

def a_propos():
    # CSS + background image
    st.markdown(f"""
        <style>
            body {{
                background-image: url("{LOGO_PATH}");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover;
            }}
            .data-card {{
                background: rgba(255, 255, 255, 0.8);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 1rem;
            }}
            .performance-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 1rem;
            }}
            .performance-table th, .performance-table td {{
                border: 1px solid #ccc;
                padding: 0.5rem;
                text-align: center;
            }}
            .highlight {{
                background-color: #d1fae5;
                font-weight: bold;
            }}
            .team-card {{
                text-align: center;
                padding: 1rem;
                background: rgba(255,255,255,0.85);
                border-radius: 10px;
                margin-top: 1rem;
            }}
            .team-photo {{
                width: 100%;
                border-radius: 10px;
                height: 200px;
                object-fit: cover;
            }}
            .metric-badge {{
                background-color: #e0f2fe;
                color: #0369a1;
                padding: 5px 10px;
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
        <div style="text-align: center; padding: 2rem;">
            <h1 style="font-size: 2.8rem; margin-bottom: 1rem;">
                🩺 Prévision du Temps de Survie du Cancer Gastrique
            </h1>
            <p style="font-size: 1.2rem; opacity: 0.9;">
                Intelligence Artificielle au service de l'oncologie clinique au Sénégal
            </p>
        </div>
        """, unsafe_allow_html=True)

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
                <div class="data-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{stat['icon']}</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #0f172a;">
                        {stat['value']}
                    </div>
                    <div style="color: #334155; font-size: 0.9rem;">
                        {stat['label']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Section Modèles de Prédiction
        st.markdown("## Performance des Modèles", unsafe_allow_html=True)

        # Tableau de performance
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

        # Visualisation des résultats
        st.markdown("## Analyse des Performances", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            try:
                st.image("assets/ibs_curve.jpeg", 
                         caption="Courbe IBS - Comparaison des modèles",
                         use_container_width=True)
            except Exception as e:
                st.error(f"Erreur de chargement de l'image: {str(e)}")
        
        with col2:
            st.markdown("""
            <div class="data-card">
                <h3 style="margin-top: 0;">Interprétation des Résultats</h3>
                <ul style="line-height: 1.8;">
                    <li>📉 Meilleure performance du modèle Deep Survival</li>
                    <li>⏱ Stabilité temporelle des prédictions</li>
                    <li>🎯 Faible erreur intégrée (IBS)</li>
                </ul>
                <div class="metric-badge">
                    🔬 Validation croisée (k=10)
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Section Équipe Scientifique
        st.markdown("## Équipe de Recherche", unsafe_allow_html=True)
        cols = st.columns(3)
        team_members = [
            {"photo": "assets/team/aba.jpeg", "name": "Pr. Aba Diop", "role": "Epidémiologiste"},
            {"photo": "assets/team/sy.jpeg", "name": "Dr. Idrissa Sy", "role": "Data Scientist"},
            {"photo": "assets/team/sefdine.jpeg", "name": "Ahmed Sefdine", "role": "Ingénieur Biomédical"}
        ]
        
        for col, member in zip(cols, team_members):
            with col:
                try:
                    st.markdown(f"""
                    <div class="team-card">
                        <img src="{member['photo']}" class="team-photo" alt="{member['name']}">
                        <h3 style="margin: 0.5rem 0; color: #0f172a;">{member['name']}</h3>
                        <p style="color: #334155; margin: 0;">{member['role']}</p>
                        <div>
                            <span class="metric-badge">🏥 CHU Dakar</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erreur d'affichage: {str(e)}")

if __name__ == "__main__":
    a_propos()
