import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── Configuration de la page ───────────────────────────────────────────────
st.set_page_config(
    page_title="Contact MED-AI",
    page_icon="📬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Configuration SMTP ─────────────────────────────────────────────────────
SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587
EMAIL_SENDER  = "votre-email@gmail.com"
EMAIL_PASSWORD= "12_SEFD"
EMAIL_RECEIVER= "sefdine668@gmail.com"

# ─── Fonctions ───────────────────────────────────────────────────────────────
def send_email(name: str, sender_email: str, message: str) -> bool:
    """Envoie un email avec un template HTML professionnel."""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_SENDER
        msg["To"]   = EMAIL_RECEIVER
        msg["Subject"] = f"📬 Nouveau contact MED-AI : {name}"

        html = f"""
        <html>
          <body style="margin:0;padding:0;font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;background:#f4f6f8;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td align="center" style="padding:40px 0;">
                  <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                    <tr>
                      <td style="padding:20px;text-align:center;border-bottom:1px solid #e0e0e0;">
                        <img src="https://i.ibb.co/logo.png" alt="MED-AI" width="120" style="display:block;margin:0 auto 10px;" />
                        <h2 style="margin:0;color:#2C3E50;font-weight:600;">Nouveau message de {name}</h2>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:30px;">
                        <p style="font-size:16px;color:#34495E;line-height:1.5;">
                          <strong>📧 Email :</strong> {sender_email}
                        </p>
                        <p style="font-size:16px;color:#34495E;line-height:1.5;">
                          <strong>📝 Message :</strong><br/>
                          <div style="background:#ecf0f1;padding:15px;border-radius:4px;margin-top:8px;">
                            {message}
                          </div>
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:20px;text-align:center;border-top:1px solid #e0e0e0;font-size:12px;color:#95A5A6;">
                        Ce message a été envoyé via le formulaire de contact MED-AI
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
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
        st.error(f"❌ Erreur lors de l'envoi de l'email : {e}")
        return False

def validate_email(email: str) -> bool:
    """Vérifie que l’email respecte le format standard."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# ─── Style global ────────────────────────────────────────────────────────────
st.markdown("""
    <style>
      :root {
        --primary: #2980B9;
        --secondary: #5D6D7E;
        --bg-light: #f4f6f8;
        --text-dark: #2C3E50;
      }
      body {
        background-color: var(--bg-light);
      }
      .contact-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
      }
      .contact-header h1 {
        color: var(--primary);
        margin-bottom: 0.5rem;
      }
      .contact-header p {
        color: var(--secondary);
        margin-top: 0;
      }
      .submit-btn button {
        background: var(--primary) !important;
        color: white !important;
        padding: 0.8rem 2rem !important;
        border-radius: 6px !important;
        font-size: 1rem !important;
      }
      .submit-btn button:hover {
        opacity: 0.9 !important;
      }
    </style>
""", unsafe_allow_html=True)

# ─── Interface ────────────────────────────────────────────────────────────────
st.markdown("<div class='contact-header' style='text-align:center;padding:2rem 0;'>", unsafe_allow_html=True)
st.markdown("## 📬 Contactez Notre Équipe Médicale")
st.markdown("> Nous vous répondons en moins de 24 heures", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

# — Formulaire de contact —
with col1:
    with st.form("contact_form"):
        st.markdown("<div class='contact-card'>", unsafe_allow_html=True)
        name    = st.text_input("Nom complet *", placeholder="Dr. Jean Dupont")
        email   = st.text_input("Email professionnel *", placeholder="contact@clinique.com")
        message = st.text_area("Message *", height=180, placeholder="Votre demande détaillée…")
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Envoyer le Message ✉️")
        if submitted:
            if not (name and email and message):
                st.error("🚨 Merci de remplir tous les champs obligatoires.")
            elif not validate_email(email):
                st.error("📧 Format d’email invalide.")
            else:
                with st.spinner("Envoi en cours…"):
                    if send_email(name, email, message):
                        st.success("✅ Votre message a bien été envoyé ! Nous revenons vers vous sous 24 h.")
                        st.balloons()

# — Info contact & réseaux —
with col2:
    st.markdown("<div class='contact-card'>", unsafe_allow_html=True)
    st.markdown("### 📌 Nos Coordonnées")
    st.markdown("""
    **Clinique MED-AI**  
    123 Rue de la Santé  
    Dakar, Sénégal  

    **Téléphone**  
    +221 77 808 09 42 (24/7)  
    """)
    st.markdown("### 🌐 Suivez-nous")
    st.markdown("""
    [🔗 LinkedIn](https://www.linkedin.com/in/sefdineahmed)  
    [🐦 Twitter](https://twitter.com/sefdineahmed)  
    [📘 Facebook](https://www.facebook.com/sefdine.ahmed)  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# — Carte interactive —
st.markdown("<div style='margin-top:2rem;'>", unsafe_allow_html=True)
st.components.v1.html("""
  <iframe 
    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3859.227291477752!2d-17.44483768468878!3d14.693534078692495!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xec1725a1bb04215%3A0x9d5f3e9d0e8e4b1e!2sDakar!5e0!3m2!1sfr!2ssn!4v1625060000000!5m2!1sfr!2ssn" 
    width="100%" height="400" style="border:0;border-radius:8px;" allowfullscreen="" loading="lazy">
  </iframe>
""", height=420)
st.markdown("</div>", unsafe_allow_html=True)

# — Pied de page —
st.markdown("""
    <div style="text-align:center;padding:1rem 0;margin-top:2rem;font-size:0.9rem;color:#7f8c8d;border-top:1px solid #ecf0f1;">
      © 2025 **MED-AI** — Propulsé par **Ahmed Sefdine**  
      <a href="https://www.linkedin.com/in/sefdineahmed" style="color:#2980B9;text-decoration:none;">LinkedIn</a> •
      <a href="https://twitter.com/sefdineahmed"       style="color:#2980B9;text-decoration:none;">Twitter</a> •
      <a href="https://www.facebook.com/sefdine.ahmed" style="color:#2980B9;text-decoration:none;">Facebook</a>
    </div>
""", unsafe_allow_html=True)
