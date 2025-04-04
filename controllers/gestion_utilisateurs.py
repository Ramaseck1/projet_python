# gestion_utilisateurs.py
from models.utilisateurs import Utilisateur

def creer_utilisateur(db, nom, email, mot_de_passe, role):
    utilisateur = Utilisateur(nom, email, mot_de_passe, role)
    utilisateur.sauvegarder(db)
    print("Utilisateur créé avec succès")