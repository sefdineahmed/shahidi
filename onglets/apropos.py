from PIL import Image
import streamlit as st
import os
import base64
from utils import LOGO_PATH # On récupère le chemin défini dans utils.py
from utils import MENU_PATH
from utils import TEAM

# Fonction pour convertir une image en base64 (utile pour le background)
def get_base64_bg(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

def a_propos():
    # Section Statistiques Clés
    st.markdown("### Principaux Indicateurs Épidémiologiques")
    cols = st.columns(3)
    stats = [
        {"icon": "🕒", "value": "58%", "label": "Survie à 5 ans"},
        {"icon": "📈", "value": "1200+", "label": "Cas annuels"},
        {"icon": "🎯", "value": "92%", "label": "Précision du modèle"}
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
    
# Section Équipe de Recherche
st.markdown("## Équipe de Recherche")
cols = st.columns(3)

TEAM_LOCAL = [
    {"photo": "assets/aba.jpeg", "name": "Pr. Aba Diop", "role": "Enseignant-Chercheur"},
    {"photo": "assets/team/sy.jpeg", "name": "Dr. Idrissa Sy", "role": "Biostatisticien"},
    {"photo": "assets/team/sefdine.jpeg", "name": "Mr. Ahmed Sefdine", "role": "Data Scientist"}
]

for col, member in zip(cols, TEAM_LOCAL):
    with col:
        if not os.path.exists(member["photo"]):
            st.error(f"Image introuvable : {member['photo']}")
        else:
            st.image(
                member["photo"],
                use_container_width=True
            )
            st.markdown(f"""
            <h4 style="text-align:center">{member['name']}</h4>
            <p style="text-align:center; color:#334155">{member['role']}</p>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    a_propos()
