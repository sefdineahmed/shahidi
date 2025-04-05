from PIL import Image
import streamlit as st
import os
import pandas as pd

LOGO_PATH = "assets/background.jpeg"  # Chemin de l'image de fond

def a_propos():
    # Nouveau CSS avec un fond en dégradé sombre et des éléments modernes
    st.markdown(f"""
        <style>
            /* Fond général en dégradé sombre */
            body {{
                background: linear-gradient(135deg, #1e1e2f, #3a3a5e);
                color: #f0f0f0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            /* Conteneur global pour une mise en page centrée */
            .main-container {{
                padding: 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }}
            /* Style des cartes de données avec ombre et bord arrondi */
            .data-card {{
                background: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            /* Tableau des performances modernisé */
            .performance-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 1rem;
                background: rgba(0,0,0,0.3);
                border-radius: 10px;
                overflow: hidden;
            }}
            .performance-table th, .performance-table td {{
                border: 1px solid #555;
                padding: 0.75rem;
                text-align: center;
            }}
            .performance-table th {{
                background: #2a2a3c;
            }}
            .performance-table td {{
                background: #1e1e2f;
            }}
            .highlight {{
                background-color: #3a8bbb;
                font-weight: bold;
            }}
            /* Style pour la section d'équipe */
            .team-card {{
                text-align: center;
                padding: 1.5rem;
                background: rgba(255,255,255,0.15);
                border-radius: 15px;
                margin-top: 1.5rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            .team-photo {{
                width: 100%;
                border-radius: 15px;
                height: 220px;
                object-fit: cover;
                margin-bottom: 0.8rem;
            }}
            /* Badge pour les indicateurs */
            .metric-badge {{
                background-color: #4caf50;
                color: #fff;
                padding: 6px 12px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 10px;
                font-size: 0.85rem;
            }}
            /* Boutons et liens */
            a {{
                color: #4caf50;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(f"""
        <div class="main-container">
            <!-- Section Héro -->
            <div style="text-align: center; padding: 2rem;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem; font-weight: bold;">
                    🩺 Prédiction du Temps de Survie du Cancer Gastrique
                </h1>
                <p style="font-size: 1.3rem; opacity: 0.8;">
                    Intelligence Artificielle au service de l'oncologie clinique au Sénégal
                </p>
            </div>

            <!-- Statistiques Clés -->
            <h2 style="text-align: center; margin-top: 2rem;">Principaux Indicateurs Épidémiologiques</h2>
            <div style="display: flex; justify-content: space-around; margin-top: 1.5rem;">
                <div class="data-card" style="flex: 1; margin: 0 0.5rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🕒</div>
                    <div style="font-size: 2.5rem; font-weight: 700;">58%</div>
                    <div style="font-size: 1rem; margin-top: 0.5rem;">Survie à 5 ans</div>
                </div>
                <div class="data-card" style="flex: 1; margin: 0 0.5rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📈</div>
                    <div style="font-size: 2.5rem; font-weight: 700;">1200+</div>
                    <div style="font-size: 1rem; margin-top: 0.5rem;">Cas annuels</div>
                </div>
                <div class="data-card" style="flex: 1; margin: 0 0.5rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
                    <div style="font-size: 2.5rem; font-weight: 700;">89%</div>
                    <div style="font-size: 1rem; margin-top: 0.5rem;">Précision du modèle</div>
                </div>
            </div>

            <!-- Performance des Modèles -->
            <h2 style="text-align: center; margin-top: 3rem;">Performance des Modèles</h2>
            <div class="data-card" style="overflow-x:auto; margin-top: 1rem;">
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

            <!-- Analyse des Performances -->
            <h2 style="text-align: center; margin-top: 3rem;">Analyse des Performances</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1.5rem;">
                <div style="flex: 2; min-width: 300px;">
                    <img src="assets/ibs_curve.jpeg" alt="Courbe IBS - Comparaison des modèles" style="width: 100%; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                </div>
                <div style="flex: 1; min-width: 250px;">
                    <div class="data-card">
                        <h3 style="margin-top: 0;">Interprétation des Résultats</h3>
                        <ul style="line-height: 1.8; text-align: left;">
                            <li>📉 Excellente performance de Deep Survival</li>
                            <li>⏱ Prédictions stables dans le temps</li>
                            <li>🎯 Faible erreur intégrée (IBS)</li>
                        </ul>
                        <div class="metric-badge">
                            🔬 Validation croisée (k=10)
                        </div>
                    </div>
                </div>
            </div>

            <!-- Équipe de Recherche -->
            <h2 style="text-align: center; margin-top: 3rem;">Équipe de Recherche</h2>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 1.5rem;">
    """, unsafe_allow_html=True)

        # Affichage des membres de l'équipe
        team_members = [
            {"photo": "assets/team/aba.jpeg", "name": "Pr. Aba Diop", "role": "Épidémiologiste"},
            {"photo": "assets/team/sy.jpeg", "name": "Dr. Idrissa Sy", "role": "Data Scientist"},
            {"photo": "assets/team/sefdine.jpeg", "name": "Ahmed Sefdine", "role": "Ingénieur Biomédical"}
        ]
        for member in team_members:
            st.markdown(f"""
                <div class="team-card" style="width: 300px; margin: 0.5rem;">
                    <img src="{member['photo']}" alt="{member['name']}" class="team-photo">
                    <h3 style="margin: 0.8rem 0 0.4rem; color: #f0f0f0;">{member['name']}</h3>
                    <p style="color: #d1d1d1;">{member['role']}</p>
                    <div>
                        <span class="metric-badge">🏥 CHU Dakar</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    a_propos()
