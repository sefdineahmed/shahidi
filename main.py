import streamlit as st
from onglets import accueil, analyse_descriptive, modelisation, a_propos, contact

# Configuration de la page
st.set_page_config(
    page_title="MOYO",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dictionnaire des pages
PAGES = {
    "🏠 Accueil": accueil,
    "📊 Analyse": analyse_descriptive,
    "🤖 Prédiction": modelisation,
    "📚 À Propos": a_propos,
    "📩 Contact": contact
}

def main():
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab"] {
            justify-content: flex-end;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    tabs = st.tabs(list(PAGES.keys()))
    for tab, (page_name, page_func) in zip(tabs, PAGES.items()):
        with tab:
            page_func()

if __name__ == "__main__":
    main()
