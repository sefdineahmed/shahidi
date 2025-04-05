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
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"📬 Nouveau contact MED-AI : {name}"

        html = f"""
        <html>
          <body style="margin: 0; font-family: 'Segoe UI', sans-serif;">
            <div style="background: #f8faff; padding: 40px;">
              <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
                <div style="padding: 40px; text-align: center;">
                  <img src="https://i.ibb.co/N3kGSkD/med-ai-logo.png" alt="MED-AI Logo" style="height: 60px; margin-bottom: 30px;">
                  <div style="background: linear-gradient(135deg, #2e77d0, #22d3ee); padding: 20px; border-radius: 12px;">
                    <h2 style="color: white; margin: 0;">Nouveau message de {name}</h2>
                  </div>
                  <div style="padding: 30px 20px; text-align: left;">
                    <p style="font-size: 16px; color: #444;"><strong>📧 Email :</strong><br>{sender_email}</p>
                    <p style="font-size: 16px; color: #444;"><strong>📝 Message :</strong></p>
                    <div style="background: #f8faff; padding: 15px; border-radius: 8px; margin-top: 10px;">
                      {message}
                    </div>
                    <hr style="border: 1px solid #eee; margin: 30px 0;">
                    <p style="font-size: 14px; color: #888; text-align: center;">
                      Ce message a été envoyé via le formulaire de contact MED-AI.
                    </p>
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
        st.error(f"❌ Erreur d'envoi : {str(e)}")
        return False

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def contact():
    st.set_page_config(page_title="Contact - MED-AI", layout="centered")

    st.markdown("""
        <style>
        body, .main {
            font-family: 'Segoe UI', sans-serif;
            background: #f8faff;
        }
        .form-container {
            max-width: 900px;
            margin: auto;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .title {
            text-align: center;
            background: linear-gradient(135deg, #2e77d0, #22d3ee);
            padding: 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
        }
        .form-style input, .form-style textarea {
            border: 2px solid #e0e7ff;
            border-radius: 12px;
            padding: 1rem;
            width: 100%;
            margin-bottom: 1.5rem;
            font-size: 1rem;
        }
        .submit-button {
            background: linear-gradient(135deg, #2e77d0, #22d3ee);
            border: none;
            border-radius: 12px;
            padding: 1rem 2rem;
            color: white;
            font-size: 1.1rem;
            cursor: pointer;
            transition: 0.3s ease;
        }
        .submit-button:hover {
            transform: scale(1.03);
            box-shadow: 0 4px 20px rgba(46,119,208,0.3);
        }
        footer {
            margin-top: 3rem;
            text-align: center;
            font-size: 0.9rem;
            color: #999;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.markdown("<div class='title'><h1>📬 Contactez l'équipe MED-AI</h1><p>Nous vous répondrons dans les 24 heures</p></div>", unsafe_allow_html=True)

    with st.form("contact_form"):
        st.markdown("<div class='form-style'>", unsafe_allow_html=True)
        name = st.text_input("Nom Complet *", placeholder="Dr. Jean Dupont")
        email = st.text_input("Email *", placeholder="contact@clinique.com")
        message = st.text_area("Message *", height=200, placeholder="Décrivez votre message ici...")
        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Envoyer le message ✉️", use_container_width=True)

    if submitted:
        if not all([name, email, message]):
            st.error("🚨 Tous les champs obligatoires (*) doivent être remplis")
        elif not validate_email(email):
            st.error("📧 Format d'email invalide")
        else:
            with st.spinner("📡 Envoi en cours..."):
                if send_email(name, email, message):
                    st.success("✅ Message envoyé avec succès !")
                    st.balloons()

    st.markdown("<footer>© 2025 MED-AI | Créé avec ❤️ par Sefdine</footer>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    contact()
