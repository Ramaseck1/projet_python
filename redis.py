class SimpleSessionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimpleSessionManager, cls).__new__(cls)
            cls._instance.redis_client = None
            # Redis n'est pas utilisé, on utilise un dictionnaire en mémoire
            cls._instance.sessions = {}
            print("Mode dictionnaire en mémoire pour les sessions")
        return cls._instance
    
    def __init__(self):
        # L'initialisation est déjà faite dans __new__
        pass
    
    def create_session(self, user_id, role):
        """Crée une nouvelle session pour un utilisateur et retourne un token"""
        import uuid
        token = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "role": role
        }
        self.sessions[token] = session_data
        return token
    
    def get_session(self, token):
        """Récupère les données d'une session à partir d'un token"""
        return self.sessions.get(token)
    
    def delete_session(self, token):
        """Supprime une session"""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False
    
    # Méthodes compatibles avec l'ancien code
    def set(self, key, value, ttl=3600):
        """Stocke une valeur avec une clé donnée"""
        self.sessions[key] = value
        return True
    
    def get(self, key):
        """Récupère une valeur à partir d'une clé"""
        return self.sessions.get(key)
    
    def delete(self, key):
        """Supprime une valeur"""
        if key in self.sessions:
            del self.sessions[key]
            return True
        return False
    
    def flush(self):
        """Vide toutes les sessions"""
        self.sessions = {}
        return True