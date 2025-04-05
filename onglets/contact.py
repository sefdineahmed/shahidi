import streamlit as st
import smtplib
import re
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Sécurité : données via st.secrets
EMAIL_SENDER = st.secrets["email"]["sender"]
EMAIL_PASSWORD = st.secrets["email"]["password"]
EMAIL_RECEIVER = st.secrets["email"]["receiver"]

# Fonction : Envoi email
def send_email(name, sender_email, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"📬 Nouveau contact MED-AI : {name}"
        
        html = f"""
        <html><body style="font-family:Segoe UI,sans-serif;">
        <div style="background:#f8faff;padding:40px;">
          <div style="max-width:600px;margin:auto;background:#fff;border-radius:16px;box-shadow:0 4px 24px rgba(0,0,0,0.08);padding:30px;">
            <h2 style="color:#2e77d0;text-align:center;">📨 Nouveau message de {name}</h2>
            <p><strong>Email :</strong> {sender_email}</p>
            <p><strong>Message :</strong><br>{message}</p>
            <hr>
            <p style="text-align:center;color:gray;font-size:0.9rem;">Formulaire de contact MED-AI</p>
          </div>
        </div></body></html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Erreur d’envoi de mail : {e}")
        return False

# Fonction : Enregistrement base de données
def save_message_to_db(name, email, message):
    try:
        conn = psycopg2.connect(
            host=st.secrets["db"]["host"],
            port=st.secrets["db"]["port"],
            dbname=st.secrets["db"]["name"],
            user=st.secrets["db"]["user"],
            password=st.secrets["db"]["password"]
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(255),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s);", (name, email, message))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Erreur de sauvegarde base : {e}")

# Validation email
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Interface Streamlit
def contact():
    st.title("📬 Contactez l'équipe MED-AI")

    name = st.text_input("Nom complet *", placeholder="Dr. Jean Dupont")
    email = st.text_input("Email professionnel *", placeholder="contact@clinique.com")
    message = st.text_area("Message *", height=200, placeholder="Décrivez votre demande...")

    if st.button("Envoyer le message ✉️"):
        if not all([name, email, message]):
            st.error("🚨 Tous les champs sont obligatoires")
        elif not validate_email(email):
            st.error("📧 Format d'email invalide")
        else:
            with st.spinner("Envoi en cours..."):
                success_email = send_email(name, email, message)
                if success_email:
                    save_message_to_db(name, email, message)
                    st.success("✅ Message envoyé et enregistré avec succès !")
                    st.balloons()

if __name__ == "__main__":
    contact()
