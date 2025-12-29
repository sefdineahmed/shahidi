import streamlit as st
import os
from utils import TEAM  # On utilise la liste définie dans utils.py pour éviter les doublons

def a_propos():
    # --- SECTION STATISTIQUES ---
    st.markdown("### 📊 Principaux Indicateurs Épidémiologiques")
    cols_stats = st.columns(3)
    stats = [
        {"icon": "🕒", "value": "58%", "label": "Survie à 5 ans"},
        {"icon": "📈", "value": "1200+", "label": "Cas annuels"},
        {"icon": "🎯", "value": "92%", "label": "Précision du modèle"}
    ]
    for col, stat in zip(cols_stats, stats):
        with col:
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 15px; text-align: center; border: 1px solid #e2e8f0;">
                <div style="font-size: 2rem;">{stat['icon']}</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #1e293b;">{stat['value']}</div>
                <div style="color: #64748b; font-size: 0.9rem;">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- SECTION PERFORMANCE ---
    st.markdown("## ⚡ Performance des Modèles")
    # ... (Le code de ton tableau reste le même, il fonctionne bien)
    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0;">
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f1f5f9;">
                    <th style="padding: 10px; border: 1px solid #ddd;">Modèle</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">C-index</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">IBS</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Random Survival Forest</td><td>0.84</td><td>0.077</td></tr>
                <tr><td>Cox PH</td><td>0.85</td><td>0.080</td></tr>
                <tr style="background-color: #d1fae5; font-weight: bold;">
                    <td>Deep Survival (Notre modèle)</td><td>0.92</td><td>0.044</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- SECTION ÉQUIPE ---
    st.markdown("## 👥 Équipe de Recherche")
    
    # AJOUT : Curseur pour régler la taille des photos
    photo_width = st.slider("Ajuster la taille des photos", min_value=100, max_value=400, value=220)

    cols_team = st.columns(3)
    
    # On boucle sur la liste TEAM importée de utils.py
    for col, member in zip(cols_team, TEAM):
        with col:
            # On vérifie si le fichier existe pour éviter un crash
            if os.path.exists(member['photo']):
                # Utilisation de st.image pour afficher la photo locale
                st.image(member['photo'], width=photo_width, use_container_width=False)
            else:
                st.warning(f"Image manquante : {member['photo']}")
            
            # Affichage des infos du membre en HTML pour le style
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h4 style="margin-bottom: 0px; color: #0f172a;">{member['name']}</h4>
                <p style="color: #64748b; font-style: italic; margin-top: 0px;">{member['role']}</p>
                <span style="background-color: #2e77d0; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.8rem;">
                    {member.get('Etablissement', 'CHU Dakar')}
                </span>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    a_propos()
