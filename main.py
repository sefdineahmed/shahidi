# main.py

import streamlit as st

# ⇦ DÉPLACÉ ICI, tout en haut avant quoi que ce soit d'autre
st.set_page_config(
    page_title="Shahidi - Prédiction de survie",
    layout="centered",
    initial_sidebar_state="expanded"
)

from onglets import accueil, analyse_descriptive, modelisation, a_propos, contact

PAGES = {
    "Accueil":    accueil,
    "Analyse":    analyse_descriptive,
    "Modélisation": modelisation,
    "À propos":   a_propos,
    "Contact":    contact
}

def main():
    menu = st.sidebar.radio("Navigation", list(PAGES.keys()))
    page_func = PAGES[menu]
    page_func()

if __name__ == "__main__":
    main()
