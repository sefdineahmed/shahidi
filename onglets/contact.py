import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration SMTP (conservée identique)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "votre-email@gmail.com"
EMAIL_PASSWORD = "12_SEFD"  
EMAIL_RECEIVER = "sefdine668@gmail.com"

def send_email(name, sender_email, message):
    """Envoie un email avec un design simplifié"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"Nouveau contact SHAHIDI-AI : {name}"
        
        # Version texte simple
        text = f"""
        Nom: {name}
        Email: {sender_email}
        Message:
        {message}
        """
        
        msg.attach(MIMEText(text, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        
        return True
    except Exception as e:
        st.error(f"Erreur d'envoi : {str(e)}")
        return False

def validate_email(email):
    """Validation d'email (identique)"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def contact():
    """Interface de contact minimaliste"""
    
    st.markdown(
        """
    <style>
        .main-container {
            max-width: 800px;
            margin: 1rem auto;
            padding: 0 1rem;
            font-family: Arial, sans-serif;
        }
        
        .contact-header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem 0;
            border-bottom: 1px solid #ddd;
        }
        
        .form-card {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .input-field {
            margin-bottom: 1.2rem;
        }
        
        .input-field label {
            display: block;
            margin-bottom: 0.4rem;
            font-weight: 500;
        }
        
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea {
            border: 1px solid #ddd !important;
            border-radius: 4px !important;
            padding: 0.8rem !important;
        }
        
        .submit-btn {
            background: #333 !important;
            color: white !important;
            padding: 0.8rem 2rem !important;
            border-radius: 4px !important;
        }
        
        .contact-info-card {
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 1rem;
        }
        
        .info-item {
            margin-bottom: 1rem;
            padding: 0.5rem 0;
        }
        
        .footer {
            text-align: center;
            padding: 1rem 0;
            margin-top: 2rem;
            color: #666;
            border-top: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        
        # En-tête simplifié
        st.markdown("""
            <div class='contact-header'>
                <h1>Contactez Notre Équipe</h1>
                <p>Nous répondons sous 24 heures</p>
            </div>
        """, unsafe_allow_html=True)

        # Grille principale
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            with st.form("contact_form"):
                st.markdown("<div class='form-card'>", unsafe_allow_html=True)
                
                name = st.text_input("Nom Complet *")
                email = st.text_input("Email *")
                message = st.text_area("Message *", height=150)
                
                submitted = st.form_submit_button("Envoyer", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            # Informations de contact simplifiées
            st.markdown("<div class='contact-info-card'>", unsafe_allow_html=True)
            st.markdown("""
                <h3>Coordonnées</h3>
                
                <div class='info-item'>
                    <p><strong>Clinique SHAHIDI-AI</strong><br>
                    123 Rue de la Santé<br>
                    Dakar, Sénégal</p>
                </div>
                
                <div class='info-item'>
                    <p><strong>Téléphone</strong><br>
                    +221 77 808 09 42</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Validation et envoi
        if submitted:
            if not all([name, email, message]):
                st.error("Tous les champs obligatoires (*) doivent être remplis")
            elif not validate_email(email):
                st.error("Format d'email invalide")
            else:
                with st.spinner("Envoi en cours..."):
                    if send_email(name, email, message):
                        st.success("Message envoyé avec succès")
                        st.balloons()

        # Pied de page simplifié
        st.markdown("""
            <div class="footer">
                <p>© 2025 MED-AI | Développé par Ahmed Sefdine</p>
            </div>
        """, unsafe_allow_html=True)
