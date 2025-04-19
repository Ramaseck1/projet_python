import bcrypt
from models.utilisateurs import Utilisateur

class GestionUtilisateurs:
    def __init__(self, db):
        self.db = db

    def ajouter_utilisateur(self, nom, email, mot_de_passe, role):
        if self.db.utilisateurs.find_one({"email": email}):
            return False, "Email déjà utilisé"
        utilisateur = Utilisateur(nom, email, mot_de_passe, role)
        utilisateur.sauvegarder(self.db)
        return True, "Utilisateur ajouté avec succès"

    def supprimer_utilisateur(self, user_id):
        from bson.objectid import ObjectId
        result = self.db.utilisateurs.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    def lister_utilisateurs(self):
        return list(self.db.utilisateurs.find())
