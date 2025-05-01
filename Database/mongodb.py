# services/mongodb_service.py
import pymongo

class MongoDBService:
    """
    Service pour gérer la connexion à MongoDB
    """
    _instance = None

    def __new__(cls):
        # Pattern Singleton pour s'assurer qu'une seule instance existe
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialise la connexion à MongoDB
        """
        try:
            self._client = pymongo.MongoClient("mongodb://localhost:27017/")
            self._db = self._client["gestion_etudiant"]
            self._collection = self._db["etudiants"]
            # Tester la connexion
            self._client.server_info()
            print("Connecté à MongoDB avec succès")
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Erreur: Impossible de se connecter à MongoDB")
            self._client = None
            self._db = None
            self._collection = None
        except Exception as e:
            print(f"Erreur lors de la connexion à MongoDB: {e}")
            self._client = None
            self._db = None
            self._collection = None

    def get_collection(self):
        """
        Retourne la collection des étudiants
        """
        return self._collection

def get_mongo_collection(self):
        """
        Ferme la connexion à MongoDB
        """
        if self._client:
            self._client.close()
            print("Connexion MongoDB fermée")