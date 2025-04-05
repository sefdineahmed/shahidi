import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "votre-email@gmail.com"
EMAIL_PASSWORD = "12_SEFD"
EMAIL_RECEIVER = "sefdine668@gmail.com"

def send_email(name, sender_email, message):
    """Envoie un email avec un style HTML professionnel et moderne"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"📬 Nouveau contact MED-AI : {name}"

        html = f"""
        <html>
          <body style="font-family: 'Segoe UI', sans-serif; background-color: #f4f8fb; padding: 40px;">
            <div style="max-width: 650px; margin: auto; background: #ffffffcc; backdrop-filter: blur(10px); border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); padding: 40px;">
              <div style="text-align: center;">
                <img src="https://i.ibb.co/6WxMPbg/med-ai-logo.png" alt="MED-AI Logo" style="height: 60px; margin-bottom: 20px;" />
                <h2 style="color: #2e77d0;">Nouveau message de {name}</h2>
              </div>
              <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
              <p style="font-size: 16px; color: #333;"><strong>✉️ Email :</strong> {sender_email}</p>
              <p style="font-size: 16px; color: #333;"><strong>📝 Message :</strong></p>
              <div style="background: #f0f4f8; padding: 15px; border-radius: 8px; color: #444;">
                {message}
              </div>
              <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
              <p style="font-size: 13px; color: #aaa; text-align: center;">
                Ce message a été envoyé via le formulaire de contact MED-AI.<br>
                <em>© 2025 MED-AI — Créé par Sefdine</em>
              </p>
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
        st.error(f"❌ Erreur d'envoi : {str(e)}")
        return False

def validate_email(email):
    """Validation avancée d'email"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def contact():
    st.set_page_config(page_title="Contact MED-AI", page_icon="📬")

    st.markdown(
        """
        <style>
            html, body {
                background-color: #f4f8fb;
            }

            .contact-container {
                max-width: 900px;
                margin: auto;
                padding: 3rem 1rem;
                font-family: 'Segoe UI', sans-serif;
            }

            .form-glass {
                background: #ffffffcc;
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 3rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
            }

            .footer {
                text-align: center;
                color: #aaa;
                margin-top: 3rem;
                font-size: 0.9rem;
            }

            .stTextInput>div>div>input,
            .stTextArea>div>div>textarea {
                border-radius: 10px !important;
                padding: 1rem !important;
                border: 2px solid #ddeaf7 !important;
                font-size: 1rem;
                transition: 0.3s;
            }

            .stTextInput>div>div>input:focus,
            .stTextArea>div>div>textarea:focus {
                border-color: #22d3ee !important;
                box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.1) !important;
            }

            .stButton>button {
                background: linear-gradient(135deg, #2e77d0, #22d3ee);
                color: white;
                padding: 0.8rem 2rem;
                border-radius: 12px;
                border: none;
                font-size: 1.1rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 14px rgba(46, 119, 208, 0.3);
            }
        </style>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='contact-container'>", unsafe_allow_html=True)
        st.image("https://i.ibb.co/6WxMPbg/med-ai-logo.png", width=120)
        st.markdown("## 📬 Contactez notre équipe médicale")
        st.markdown("**Une question ? Un projet ? Nous vous répondons sous 24h.**")

        with st.form("contact_form"):
            st.markdown("<div class='form-glass'>", unsafe_allow_html=True)
            name = st.text_input("👤 Nom Complet *", placeholder="Dr. Jean Dupont")
            email = st.text_input("📧 Email Professionnel *", placeholder="contact@exemple.com")
            message = st.text_area("📝 Message *", height=200, placeholder="Décrivez votre demande...")

            submitted = st.form_submit_button("Envoyer le Message ✉️")
            st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not all([name, email, message]):
                st.error("🚨 Tous les champs obligatoires (*) doivent être remplis")
            elif not validate_email(email):
                st.error("📧 Format d'email invalide")
            else:
                with st.spinner("⏳ Envoi en cours..."):
                    if send_email(name, email, message):
                        st.success("✅ Message envoyé avec succès ! Nous vous répondrons sous 24h.")
                        st.balloons()

        st.markdown("<div class='footer'>© 2025 MED-AI — Créé avec ❤️ par Sefdine</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    contact()
