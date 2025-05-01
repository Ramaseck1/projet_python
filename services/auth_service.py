import redis
import bcrypt
import uuid
from models.utilisateurs import Utilisateur
from Database.redis import SimpleSessionManager

class AuthService:
    def __init__(self, db):
        self.db = db
        self.session_manager = SimpleSessionManager()

    def login(self, email, mot_de_passe):
        utilisateur = self.db.utilisateurs.find_one({"email": email})
        if utilisateur:
            try:
                if bcrypt.checkpw(mot_de_passe.encode(), utilisateur["mot_de_passe"].encode()):
                    user_id = str(utilisateur.get("_id"))
                    role = utilisateur["role"]
                    token = self.session_manager.create_session(user_id, role)
                    return token, role,user_id
            except Exception as e:
                print(f"Erreur lors de la vérification du mot de passe: {e}")
        return None, None , None

    def logout(self, token):
        self.session_manager.delete_session(token)
        return True

    def is_authenticated(self, token):
        session = self.session_manager.get_session(token)
        if session:
            user_id = session["user_id"]
            try:
                from bson.objectid import ObjectId
                utilisateur = self.db.utilisateurs.find_one({"_id": ObjectId(user_id)})
            except:
                utilisateur = self.db.utilisateurs.find_one({"_id": user_id})
            
            if utilisateur:
                return True, session["role"]
        return False, None

    def register(self, nom, email, mot_de_passe, role="etudiant"):
        # Vérifier si l'email existe déjà
        if self.db.utilisateurs.find_one({"email": email}):
            return False, "Email déjà utilisé"
        
        # Créer un nouvel utilisateur avec la classe Utilisateur
        utilisateur = Utilisateur(nom, email, mot_de_passe, role)
        utilisateur.sauvegarder(self.db)
        return True, "Inscription réussie"

# Fonction pour assurer qu'un compte administrateur existe
def ensure_admin_exists(db):
    admin = db.utilisateurs.find_one({"role": "admin"})
    if not admin:
        print("Création d'un compte administrateur par défaut...")
        auth_service = AuthService(db)
        auth_service.register("Admin", "admin@example.com", "admin123", "admin")
        print("Compte administrateur créé: admin@example.com / admin123")