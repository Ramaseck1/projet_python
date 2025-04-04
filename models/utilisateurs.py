import bcrypt
import uuid
from pymongo import MongoClient

class Utilisateur:
    def __init__(self, nom, email, mot_de_passe, role):
        self.id = str(uuid.uuid4())
        self.nom = nom
        self.email = email
        self.mot_de_passe = self.hasher_mot_de_passe(mot_de_passe)
        self.role = role  # "admin", "enseignant", "etudiant"

    def hasher_mot_de_passe(self, mot_de_passe):
        return bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt()).decode()

    def verifier_mot_de_passe(self, mot_de_passe):
        return bcrypt.checkpw(mot_de_passe.encode(), self.mot_de_passe.encode())
    
    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,
            "role": self.role
        }

    def sauvegarder(self, db):
        collection = db["utilisateurs"]
        collection.insert_one(self.to_dict())
