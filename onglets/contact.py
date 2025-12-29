import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration SMTP (Utilisez st.secrets pour la production)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = st.secrets.get("EMAIL_SENDER", "votre-email@gmail.com")
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", "votre-mot-de-passe") 
EMAIL_RECEIVER = "sefdine668@gmail.com"

def send_email(name, sender_email, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"🚀 Nouveau contact SHAHIDI-AI : {name}"
        
        html = f"""
        <html>
          <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; line-height: 1.6;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden;">
              <div style="background: #2e77d0; padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">SHAHIDI-AI</h1>
              </div>
              <div style="padding: 30px;">
                <h2 style="color: #2e77d0; border-bottom: 2px solid #f0f4f8; padding-bottom: 10px;">Nouvelle Demande</h2>
                <p><strong>Nom :</strong> {name}</p>
                <p><strong>Email :</strong> {sender_email}</p>
                <div style="background: #f9f9f9; padding: 20px; border-left: 4px solid #2e77d0; margin-top: 20px;">
                  <p style="margin: 0;">{message}</p>
                </div>
              </div>
              <div style="background: #f4f7f9; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                Ce message a été généré par le portail SHAHIDI-AI
              </div>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        return True
    except Exception as e:
        return False

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def contact():
    # --- CSS PROFESSIONNEL ---
    st.markdown("""
        <style>
            .contact-header {
                background: linear-gradient(135deg, #1e3a8a 0%, #2e77d0 100%);
                color: white;
                padding: 3rem 2rem;
                border-radius: 20px;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }
            .form-card {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border: 1px solid #f0f4f8;
            }
            .contact-info-card {
                background: #f8fafc;
                padding: 2rem;
                border-radius: 15px;
                height: 100%;
                border-left: 5px solid #2e77d0;
            }
            .info-item {
                margin-bottom: 1.5rem;
                display: flex;
                align-items: flex-start;
                gap: 10px;
            }
            .footer {
                text-align: center;
                padding: 2rem;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
                margin-top: 3rem;
            }
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                border-radius: 8px !important;
            }
            .map-container {
                margin-top: 3rem;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # --- CONTENU ---
    st.markdown("""
        <div class='contact-header'>
            <h1 style="color: white; margin: 0;">Parlons de votre projet</h1>
            <p style="font-size: 1.1rem; opacity: 0.9; margin-top: 10px;">
                Expertise en IA médicale et analyse de survie au service de vos patients.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.8, 1], gap="large")
    
    with col1:
        st.markdown("### ✉️ Envoyez-nous un message")
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Nom Complet *", placeholder="Ex: Dr. Jean Dupont")
            email = st.text_input("Email Professionnel *", placeholder="jean.dupont@chu-dakar.sn")
            message = st.text_area("Votre Message *", height=180, placeholder="Comment pouvons-nous vous aider ?")
            
            submitted = st.form_submit_button("🚀 Envoyer la demande")

    with col2:
        st.markdown("### 📍 Informations")
        st.markdown(f"""
            <div class='contact-info-card'>
                <div class='info-item'>
                    <div>
                        <h4 style="margin:0; color:#1e3a8a;">Siège Social</h4>
                        <p style="color:#64748b;">Clinique Shahidi, 123 Rue de la Santé<br>Dakar, Sénégal</p>
                    </div>
                </div>
                <div class='info-item'>
                    <div>
                        <h4 style="margin:0; color:#1e3a8a;">Contact Direct</h4>
                        <p style="color:#64748b;">+221 77 808 09 42<br>contact@shahidi-ai.sn</p>
                    </div>
                </div>
                <div class='info-item'>
                    <div>
                        <h4 style="margin:0; color:#1e3a8a;">Support Technique</h4>
                        <p style="color:#64748b;">Disponible 24j/7 pour les urgences médicales.</p>
                    </div>
                </div>
                <hr style="border:0; border-top:1px solid #e2e8f0;">
                <h4 style="color:#1e3a8a;">Suivez-nous</h4>
                <div style="display: flex; gap: 15px;">
                    <a href="https://linkedin.com/in/sefdineahmed" style="text-decoration:none;">🔵 LinkedIn</a>
                    <a href="#" style="text-decoration:none;">⚫ Twitter / X</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Logique d'envoi
    if submitted:
        if not name or not email or not message:
            st.warning("⚠️ Veuillez remplir tous les champs obligatoires.")
        elif not validate_email(email):
            st.error("❌ L'adresse email n'est pas valide.")
        else:
            with st.spinner("Transmission sécurisée en cours..."):
                if send_email(name, email, message):
                    st.success("✅ Votre message a été transmis avec succès. Notre équipe vous recontactera sous 24h.")
                    st.balloons()
                else:
                    st.error("❌ Une erreur technique est survenue. Veuillez nous contacter directement par téléphone.")

    # Carte et Footer
    st.markdown("### 🗺️ Localisation")
    st.markdown("""
        <div class='map-container'>
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3858.966752317112!2d-17.467686685158145!3d14.713437589729864!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTTCsDQyJzQ4LjQiTiAxN8KwMjcnNTUuOCJX!5e0!3m2!1sfr!2ssn!4v1625123456789" 
                width="100%" height="350" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        </div>
        <div class='footer'>
            © 2025 <b>SHAHIDI-AI</b> | Développé avec excellence par Ahmed Sefdine<br>
            <small>Données sécurisées et conformes aux protocoles médicaux</small>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    contact()
