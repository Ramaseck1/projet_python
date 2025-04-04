import smtplib

def envoyer_notification(email, sujet, message):
    serveur = smtplib.SMTP("smtp.gmail.com", 587)
    serveur.starttls()
    serveur.login("votre_email@gmail.com", "mot_de_passe")
    email_message = f"Subject: {sujet}\n\n{message}"
    serveur.sendmail("votre_email@gmail.com", email, email_message)
    serveur.quit()
