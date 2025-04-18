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
    """Envoie un email avec un design HTML professionnel"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"📬 Nouveau contact SHAHIDI-AI : {name}"
        
        html = f"""
        <html>
          <body style="margin: 0; font-family: 'Segoe UI', sans-serif;">
            <div style="background: #f8faff; padding: 40px;">
              <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08);">
                <div style="padding: 40px; text-align: center;">
                  <img src="https://i.ibb.co.com/logo.png" alt="MED-AI Logo" style="height: 60px; margin-bottom: 30px;">
                  <div style="background: linear-gradient(135deg, #2e77d0, #22d3ee); padding: 20px; border-radius: 12px;">
                    <h2 style="color: white; margin: 0;">Nouveau message de {name}</h2>
                  </div>
                  <div style="padding: 30px 20px; text-align: left;">
                    <p style="font-size: 16px; color: #444;">
                        <strong style="color: #2e77d0;">📧 Email :</strong><br>{sender_email}
                    </p>
                    <p style="font-size: 16px; color: #444;">
                        <strong style="color: #2e77d0;">📝 Message :</strong>
                    </p>
                    <div style="background: #f8faff; padding: 15px; border-radius: 8px;">
                        {message}
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
    """Validation avancée d'email"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def contact():
    """Interface de contact professionnelle"""
    
    st.set_page_config(page_title="Contact SHAHIDI-AI", layout="wide")
    
    # Appliquer le CSS personnalisé
    with open("styles.css", "r") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class='contact-header'>
                <h1>📬 Contactez Notre Équipe Médicale</h1>
                <p>Une question ? Un projet ? Nous répondons sous 24h</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            with st.form("contact_form"):
                st.markdown("<div class='form-card'>", unsafe_allow_html=True)

                name = st.text_input("Nom Complet *", placeholder="Dr. Jean Dupont")
                email = st.text_input("Email Professionnel *", placeholder="contact@clinique.com")
                message = st.text_area("Message *", height=200, placeholder="Décrivez votre demande en détail...")
                
                submitted = st.form_submit_button("Envoyer le Message ✉️", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='contact-info-card'>", unsafe_allow_html=True)
            st.markdown("""
                <h3>📌 Coordonnées</h3>
                <div class='info-item'>🏥 <div><strong>Clinique MED-AI</strong><br>123 Rue de la Santé<br>Dakar, Sénégal</div></div>
                <div class='info-item'>📞 <div><strong>Téléphone</strong><br>+221 77 808 09 42</div></div>
                <div class='info-item'>🌐 <div>
                    <strong>Réseaux Sociaux</strong><br>
                    <a href="https://www.linkedin.com/in/sefdineahmed" target="_blank">🔗 LinkedIn</a> |
                    <a href="https://twitter.com/sefdineahmed" target="_blank">🐦 Twitter</a> |
                    <a href="https://www.facebook.com/sefdine.ahmed" target="_blank">📘 Facebook</a>
                </div></div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not all([name, email, message]):
                st.error("🚨 Tous les champs obligatoires (*) doivent être remplis")
            elif not validate_email(email):
                st.error("📧 Format d'email invalide")
            else:
                with st.spinner("Envoi en cours..."):
                    if send_email(name, email, message):
                        st.success("✅ Message envoyé avec succès ! Nous vous répondrons sous 24h.")
                        st.balloons()

        st.markdown("""
            <div class='map-container'>
                <iframe 
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3859.227291477752!2d-17.44483768468878!3d14.693534078692495!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xec1725a1bb04215%3A0x9d5f3e9d0e8e4b1e!2sDakar!5e0!3m2!1sfr!2ssn!4v1625060000000!5m2!1sfr!2ssn" 
                    width="100%" 
                    height="400" 
                    style="border:0;" 
                    allowfullscreen="" 
                    loading="lazy">
                </iframe>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="footer">
                <p>
                    © 2025 <strong>MED-AI</strong> | Propulsé par <strong>Ahmed Sefdine</strong><br>
                    Suivez-nous :
                    <a href="https://www.linkedin.com/in/sefdineahmed" target="_blank">🔗 LinkedIn</a>
                    <a href="https://twitter.com/sefdineahmed" target="_blank">🐦 Twitter</a>
                    <a href="https://www.facebook.com/sefdine.ahmed" target="_blank">📘 Facebook</a>
                </p>
            </div>
        """, unsafe_allow_html=True)

# Appel de la fonction principale
if __name__ == "__main__":
    contact()
