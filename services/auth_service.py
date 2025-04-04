# services/auth_service.py
import redis
from models.utilisateurs import Utilisateur

class AuthService:
    def __init__(self, db):
        self.db = db
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def login(self, email, mot_de_passe):
        utilisateur = self.db.utilisateurs.find_one({"email": email})
        if utilisateur and bcrypt.checkpw(mot_de_passe.encode(), utilisateur["mot_de_passe"].encode()):
            token = str(uuid.uuid4())
            self.redis_client.setex(f"session:{token}", 3600, utilisateur["id"])
            return token
        return None

    def logout(self, token):
        self.redis_client.delete(f"session:{token}")