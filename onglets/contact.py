import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ Cette ligne doit être en tout premier
st.set_page_config(page_title="Contact MED-AI", page_icon="📬")

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "votre-email@gmail.com"       # Remplace par ton adresse
EMAIL_PASSWORD = "12_SEFD"                   # ⚠️ À sécuriser avec st.secrets si possible
EMAIL_RECEIVER = "sefdine668@gmail.com"

def send_email(name, sender_email, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"📬 Nouveau contact MED-AI : {name}"
        
        html = f"""
        <html>
          <body style="margin: 0; font-family: 'Segoe UI', sans-serif;">
            <div style="background: #f8faff; padding: 40px;">
              <div style="max-width: 600px; margin: auto; background: white; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
                <div style="padding: 40px; text-align: center;">
                  <img src="https://i.ibb.co.com/logo.png" alt="MED-AI Logo" style="height: 60px; margin-bottom: 30px;">
                  <div style="background: linear-gradient(135deg, #2e77d0, #22d3ee); padding: 20px; border-radius: 12px;">
                    <h2 style="color: white; margin: 0;">Nouveau message de {name}</h2>
                  </div>
                  <div style="padding: 30px 20px; text-align: left;">
                    <p style="font-size: 16px; color: #444;"><strong>Email :</strong> {sender_email}</p>
                    <p style="font-size: 16px; color: #444;"><strong>Message :</strong><br>{message}</p>
                    <hr style="margin: 30px 0;">
                    <p style="font-size: 14px; color: #888; text-align: center;">Ce message a été envoyé via le formulaire de contact MED-AI</p>
                  </div>
                </div>
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
        st.error(f"❌ Erreur lors de l'envoi : {str(e)}")
        return False

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def contact():
    st.markdown("""
    <style>
        :root {
            --primary: #2e77d0;
            --secondary: #1d5ba6;
            --accent: #22d3ee;
        }

        .main-container {
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
            font-family: 'Segoe UI', sans-serif;
        }

        .contact-header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 16px;
            color: #fff;
        }

        .form-card {
            background: #f8faff;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }

        .input-field label {
            margin-bottom: 0.6rem;
            color: var(--primary);
            font-weight: 500;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(46, 119, 208, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Titre principal
    st.markdown("""
        <div class='contact-header'>
            <h1>📬 Contactez MED-AI</h1>
            <p>Vous avez une question, une suggestion ou une collaboration ? Écrivez-nous !</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form("contact_form"):
            st.markdown("<div class='form-card'>", unsafe_allow_html=True)

            name = st.text_input("Nom Complet *", placeholder="Dr. Jean Dupont")
            email = st.text_input("Email *", placeholder="exemple@medai.com")
            message = st.text_area("Message *", height=200, placeholder="Écrivez votre message ici...")

            submitted = st.form_submit_button("Envoyer le Message ✉️")

            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:white; padding:2rem; border-radius:12px; box-shadow:0 4px 24px rgba(0,0,0,0.05);'>
            <h3 style='color: var(--primary);'>📍 Coordonnées</h3>
            <p><strong>Adresse :</strong><br>123 Rue de la Santé, Dakar</p>
            <p><strong>Téléphone :</strong><br>+221 77 808 09 42</p>
            <p><strong>Email :</strong><br>contact@med-ai.com</p>
            <h4 style='margin-top:2rem; color:var(--primary);'>🌐 Suivez-nous</h4>
            <p>
                <a href="https://www.linkedin.com/in/sefdineahmed" target="_blank">🔗 LinkedIn</a><br>
                <a href="https://twitter.com/sefdineahmed" target="_blank">🐦 Twitter</a><br>
                <a href="https://www.facebook.com/sefdine.ahmed" target="_blank">📘 Facebook</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

    if submitted:
        if not all([name, email, message]):
            st.error("🚨 Tous les champs obligatoires (*) doivent être remplis")
        elif not validate_email(email):
            st.error("📧 Format d'email invalide")
        else:
            with st.spinner("Envoi du message..."):
                if send_email(name, email, message):
                    st.success("✅ Message envoyé avec succès ! Nous reviendrons vers vous sous 24h.")
                    st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)

# Appel de la fonction
contact()
