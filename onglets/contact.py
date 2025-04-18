import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_CONFIG  # Configuration externalisée

# Configuration initiale (à remplacer par des variables d'environnement en production)
EMAIL_SENDER = SMTP_CONFIG["sender"]
EMAIL_PASSWORD = SMTP_CONFIG["password"]
EMAIL_RECEIVER = SMTP_CONFIG["receiver"]

def send_email(name, sender_email, message):
    """Envoi sécurisé d'email avec template professionnel"""
    try:
        # Création du message MIME
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"MED-AI - Nouveau message de {name}"
        
        # Template HTML professionnel
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ margin: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
                    .header {{ background: #1a365d; padding: 40px; color: white; }}
                    .content {{ padding: 40px 20px; line-height: 1.6; color: #444; }}
                    .message-box {{ background: #f8f9fa; border-left: 4px solid #2b6cb0; padding: 15px; margin: 20px 0; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; font-size: 0.9em; color: #666; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1 style="margin:0; font-weight:300;">MED-AI Contact</h1>
                    <p style="margin:5px 0 0; font-size:0.9em;">Plateforme d'Intelligence Médicale</p>
                </div>
                
                <div class="content">
                    <h2 style="color: #2b6cb0; margin-top:0;">Nouveau message</h2>
                    <p><strong>Expéditeur:</strong> {name} &lt;{sender_email}&gt;</p>
                    <div class="message-box">
                        {message}
                    </div>
                </div>
                
                <div class="footer">
                    <p>Cet email a été généré automatiquement - Ne pas répondre directement</p>
                    <p style="margin:5px 0;">© 2024 MED-AI. Tous droits réservés.</p>
                </div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, "html"))

        # Connexion sécurisée au serveur SMTP
        with smtplib.SMTP(SMTP_CONFIG["server"], SMTP_CONFIG["port"]) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            
        return True
    except Exception as e:
        st.error(f"Erreur d'envoi : {str(e)}")
        return False

def validate_email(email):
    """Validation robuste d'adresse email"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def main():
    """Interface utilisateur professionnelle"""
    
    # Configuration du style CSS
    st.markdown("""
    <style>
        :root {{
            --primary: #1a365d;
            --secondary: #2b6cb0;
            --accent: #4299e1;
        }}
        
        .main {{ max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
        
        .contact-header {{
            text-align: center;
            margin: 3rem 0;
            padding: 2rem;
            background: var(--primary);
            border-radius: 10px;
            color: white;
        }}
        
        .form-card {{
            background: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        
        .stTextInput input, .stTextArea textarea {{
            border: 1px solid #e2e8f0 !important;
            border-radius: 6px !important;
            padding: 0.8rem !important;
        }}
        
        .stButton button {{
            background: var(--secondary) !important;
            color: white !important;
            padding: 0.8rem 2rem !important;
            border-radius: 6px !important;
            transition: all 0.3s !important;
        }}
        
        .stButton button:hover {{
            background: var(--primary) !important;
            transform: translateY(-1px);
        }}
        
        .contact-info {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1.5rem 0;
        }}
        
        .success-message {{
            background: #f0fff4;
            color: #2f855a;
            padding: 1rem;
            border-radius: 6px;
            border-left: 4px solid #38a169;
            margin: 1rem 0;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Structure de la page
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # En-tête
    st.markdown("""
        <div class="contact-header">
            <h1>Contactez notre équipe</h1>
            <p>Nous répondons sous 24 heures ouvrées</p>
        </div>
    """, unsafe_allow_html=True)

    # Contenu principal
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        with st.form("contact_form"):
            st.markdown('<div class="form-card">', unsafe_allow_html=True)
            
            st.subheader("Formulaire de contact")
            name = st.text_input("Nom complet*", placeholder="Dr. Jean Dupont")
            email = st.text_input("Email professionnel*", placeholder="contact@etablissement.com")
            message = st.text_area("Message*", height=150, 
                                 placeholder="Décrivez votre demande en détail...")
            
            submitted = st.form_submit_button("Envoyer", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="contact-info">
                <h3>Coordonnées</h3>
                <p>📌 <strong>Siège social</strong><br>
                123 Rue de la Santé<br>
                Dakar, Sénégal</p>
                
                <p>📞 <strong>Téléphone</strong><br>
                +221 77 808 09 42</p>
                
                <p>🕒 <strong>Horaires</strong><br>
                Lun-Ven : 8h-18h</p>
                
                <h3>Réseaux sociaux</h3>
                <p>
                    <a href="https://linkedin.com/company" target="_blank" style="color: var(--secondary);">LinkedIn</a> •
                    <a href="https://twitter.com" target="_blank" style="color: var(--secondary);">Twitter</a> •
                    <a href="https://facebook.com" target="_blank" style="color: var(--secondary);">Facebook</a>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Gestion de la soumission
    if submitted:
        if not all([name, email, message]):
            st.error("Veuillez remplir tous les champs obligatoires (*)")
        elif not validate_email(email):
            st.error("Veuillez entrer une adresse email valide")
        else:
            with st.spinner("Envoi en cours..."):
                if send_email(name, email, message):
                    st.markdown("""
                        <div class="success-message">
                            ✅ Votre message a été envoyé avec succès.<br>
                            <small>Nous vous répondrons dans les plus brefs délais.</small>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()

    # Pied de page
    st.markdown("""
        <div style="text-align: center; margin: 4rem 0 2rem; color: #666;">
            <hr style="margin: 2rem 0;">
            <p>© 2024 MED-AI • Tous droits réservés<br>
            <small>Conformité RGPD • Sécurité des données médicales</small></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
