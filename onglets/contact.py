import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "votre-email@gmail.com"
EMAIL_PASSWORD = "12_SEFD"  # Sécurisez cela !
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
                  <img src='https://i.ibb.co/y0YVKXC/med-ai-logo.png' alt='MED-AI Logo' style='height: 60px; margin-bottom: 30px;'>
                  <div style="background: linear-gradient(135deg, #2e77d0, #22d3ee); padding: 20px; border-radius: 12px;">
                    <h2 style="color: white; margin: 0;">Nouveau message de {name}</h2>
                  </div>
                  <div style="padding: 30px 20px; text-align: left;">
                    <div style="margin-bottom: 25px;">
                      <p style="font-size: 16px; color: #444; margin: 8px 0;">
                        <strong style="color: #2e77d0;">📧 Email :</strong><br>{sender_email}
                      </p>
                      <p style="font-size: 16px; color: #444; margin: 8px 0;">
                        <strong style="color: #2e77d0;">📝 Message :</strong><br>
                        <div style="background: #f0f4ff; padding: 15px; border-radius: 8px; margin-top: 10px; color:#333;">
                          {message}
                        </div>
                      </p>
                    </div>
                    <hr style="border: 1px solid #eee; margin: 30px 0;">
                    <p style="font-size: 14px; color: #888; text-align: center;">
                      Ce message a été envoyé via le formulaire de contact MED-AI
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
    st.markdown("""
    <style>
        .contact-header {
            text-align: center;
            background: linear-gradient(135deg, #2e77d0, #22d3ee);
            color: white;
            padding: 2rem;
            border-radius: 16px;
        }
        .form-card {
            background: #ffffffcc;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        .form-footer {
            text-align:center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #999;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='contact-header'>
        <h1>📬 Contactez MED-AI</h1>
        <p>Nous vous répondrons dans les 24h</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("contact_form"):
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        name = st.text_input("Nom Complet *", placeholder="Dr. Jean Dupont")
        email = st.text_input("Email *", placeholder="contact@exemple.com")
        message = st.text_area("Message *", height=200, placeholder="Votre message...")
        submitted = st.form_submit_button("Envoyer le Message ✉️")
        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not all([name, email, message]):
            st.error("🚨 Tous les champs obligatoires (*) doivent être remplis")
        elif not validate_email(email):
            st.error("📧 Format d'email invalide")
        else:
            with st.spinner("Envoi en cours..."):
                if send_email(name, email, message):
                    st.success("✅ Message envoyé avec succès. Nous vous répondrons bientôt !")
                    st.balloons()

    st.markdown("""
    <div class='form-footer'>
        © 2025 MED-AI | Créé avec ❤️ par Sefdine
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    contact()
