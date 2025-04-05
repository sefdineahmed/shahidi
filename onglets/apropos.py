from PIL import Image
import streamlit as st
import os
import pandas as pd

LOGO_PATH = "assets/background.jpeg"  # Chemin de l'image de fond

def a_propos():
    # CSS personnalisé avec un style moderne et dynamique
    st.markdown(f"""
        <style>
            /* Background global */
            body {{
                background-image: url("{LOGO_PATH}");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #f0f0f0;
            }}
            /* Effet de superposition pour adoucir le background */
            .overlay {{
                background: rgba(0, 0, 0, 0.6);
                padding: 2rem;
                border-radius: 10px;
                margin: 1rem 0;
            }}
            /* Style des cartes de données */
            .data-card {{
                background: rgba(255, 255, 255, 0.15);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 1rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            /* Style du tableau de performance */
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
            /* Style des cartes équipe */
            .team-card {{
                text-align: center;
                padding: 1rem;
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
                margin-top: 1rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            .team-photo {{
                width: 100%;
                border-radius: 10px;
                height: 220px;
                object-fit: cover;
                border: 3px solid #2e77d0;
            }}
            /* Badge pour les métriques */
            .metric-badge {{
                background-color: #2e77d0;
                color: #fff;
                padding: 6px 12px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 10px;
                font-size: 0.85rem;
            }}
            /* Titres et textes */
            h1, h2, h3 {{
                color: #ffffff;
            }}
            p, li {{
                color: #d1d5db;
            }}
            /* Effet hover pour les cartes */
            .data-card:hover, .team-card:hover {{
                transform: translateY(-5px);
                transition: transform 0.3s ease;
            }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        # Section Héro
        st.markdown("""
        <div class="overlay" style="text-align: center;">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">
                🩺 Prévision du Temps de Survie du Cancer Gastrique
            </h1>
            <p style="font-size: 1.3rem; opacity: 0.9;">
                L'intelligence artificielle au service de l'oncologie clinique au Sénégal
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Section Statistiques Clés
        st.markdown("<h2>Principaux Indicateurs Épidémiologiques</h2>", unsafe_allow_html=True)
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
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{stat['icon']}</div>
                    <div style="font-size: 2.2rem; font-weight: 700;">
                        {stat['value']}
                    </div>
                    <div style="font-size: 1rem;">
                        {stat['label']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Section Modèles de Prédiction
        st.markdown("<h2>Performance des Modèles</h2>", unsafe_allow_html=True)

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
        st.markdown("<h2>Analyse des Performances</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            try:
                st.image("assets/ibs_curve.jpeg", 
                         caption="Courbe IBS - Comparaison des modèles",
                         use_container_width=True)
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
                <div class="metric-badge">
                    🔬 Validation croisée (k=10)
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Section Équipe Scientifique
        st.markdown("<h2>Équipe de Recherche</h2>", unsafe_allow_html=True)
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
                    <div class="team-card">
                        <img src="{member['photo']}" class="team-photo" alt="{member['name']}">
                        <h3 style="margin: 0.5rem 0;">{member['name']}</h3>
                        <p style="margin: 0;">{member['role']}</p>
                        <div>
                            <span class="metric-badge">🏥 CHU Dakar</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erreur d'affichage : {str(e)}")

if __name__ == "__main__":
    a_propos()
