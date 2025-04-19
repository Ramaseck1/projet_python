import pymongo
from services.auth_service import AuthService
from models.etudiant import Etudiant
from services.gestion_etudiants import GestionEtudiants
from services.statistiques_service import StatistiquesService
from services.notification_service import envoyer_notification


def get_db_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["gestion_etudiant"]

def afficher_menu_principal():
    print("\n===== Gestion des Étudiants =====")
    print("1. S'inscrire")
    print("2. Se connecter")
    print("0. Quitter")
    return input("Votre choix: ")

def afficher_menu_connecte(role):
    print(f"\n===== Menu {role.capitalize()} =====")
    if role == "admin":
        print("1. Gérer les utilisateurs")
        print("2. Gérer les étudiants")
        print("3. Statistiques & rapports")
        print("4. Mon profil")
        print("5. Se déconnecter")
        print("0. Quitter")
    elif role == "enseignant":
        print("1. Gérer les étudiants")
        print("2. Mon profil")
        print("3. Se déconnecter")
        print("0. Quitter")
    elif role == "etudiant":
        print("1. Voir mes notes")
        print("2. Mon profil")
        print("3. Se déconnecter")
        print("0. Quitter")
    return input("Votre choix: ")

def afficher_menu_etudiants():
    print("\n===== Gestion des Étudiants =====")
    print("1. Ajouter un étudiant")
    print("2. Rechercher un étudiant")
    print("3. Afficher tous les étudiants")
    print("4. Trier par moyenne")
    print("5. Modifier les notes")
    print("6. Supprimer un étudiant")
    print("7. Exporter les données")
    print("8. Recherche multi-critère")
    print("0. Retour")
    return input("Votre choix: ")

def afficher_menu_statistiques():
    print("\n===== Statistiques et Rapports =====")
    print("1. Moyenne générale d'une classe")
    print("2. Top 10 des étudiants")
    print("3. Générer rapport PDF")
    print("0. Retour")
    return input("Votre choix: ")

def menu_inscription(auth_service):
    print("\n===== Inscription =====")
    nom = input("Nom: ")
    email = input("Email: ")
    mot_de_passe = input("Mot de passe: ")
    
    print("Rôles disponibles:")
    print("1. Étudiant")
    print("2. Enseignant")
    print("3. admin")
     
    choix = input("Choisissez un rôle (1-3): ")
    if choix == "2":
        role = "enseignant"
    elif choix == "3":
        role = "admin"
    else:
        role = "etudiant"
        
    success, message = auth_service.register(nom, email, mot_de_passe, role)
    print(message)
    return success
   
def menu_connexion(auth_service):
    print("\n===== Connexion =====")
    email = input("Email: ")
    mot_de_passe = input("Mot de passe: ")
    
    token, role, utilisateur_id = auth_service.login(email, mot_de_passe)
    if token:
        print("Connexion réussie!")
        return token, role, utilisateur_id
    else:
        print("Échec de connexion. Vérifiez vos identifiants.")
        return None, None, None

def gerer_etudiants(db, utilisateur_id=None, role="admin"):
    gestion = GestionEtudiants(db)

    while True:
        choix = afficher_menu_etudiants()
        
        if choix == "1":
            if role not in ["admin", "enseignant"]:
                print("Seuls un administrateur ou un enseignant peuvent ajouter un étudiant.")
                continue
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            telephone = input("Téléphone: ")
            classe = input("Classe: ")
            try:
                notes_input = input("Notes (séparées par des virgules): ")
                notes = [float(note) for note in notes_input.split(",")]
                etudiant = Etudiant(nom=nom, prenom=prenom, telephone=telephone, classe=classe, notes=notes)
                gestion.ajouter_etudiant(etudiant)
            except ValueError:
                print("Erreur: Format de notes invalide")

        elif choix == "2":
            nom = input("Nom de l'étudiant à rechercher: ")
            gestion.rechercher_etudiant(nom)

        elif choix == "3":
            gestion.afficher_etudiants()

        elif choix == "4":
            gestion.trier_par_moyenne()

        elif choix == "5":
            telephone = input("Téléphone de l'étudiant: ")
            try:
                notes_input = input("Nouvelles notes (séparées par des virgules): ")
                notes = [float(note) for note in notes_input.split(",")]
                gestion.modifier_notes(telephone, notes)
            except ValueError:
                print("Erreur: Format de notes invalide")

        elif choix == "6":
            telephone = input("Téléphone de l'étudiant à supprimer: ")
            gestion.supprimer_etudiant(telephone)

        elif choix == "7":
            format_export = input("Format d'exportation (csv/json/excel/pdf): ").lower()
            gestion.exporter_donnees(format_export)

        elif choix == "8":
            fichier = input("Chemin du fichier à importer (CSV ou Excel): ")
            gestion.importer_donnees(fichier)

        elif choix == "9":
            critere = input("Critère (nom, prenom, classe, etc.): ")
            valeur = input("Valeur: ")
            gestion.recherche_multi_critere(critere, valeur)

        elif choix == "0":
            break
        else:
            print("Option invalide.")

def menu_statistiques(db):
    stats = StatistiquesService(db)

    while True:
        choix = afficher_menu_statistiques()

        if choix == "1":
            classe = input("Classe: ")
            moyenne = stats.moyenne_generale_classe(classe)
            if moyenne is not None:
                print(f"Moyenne générale de {classe} : {moyenne:.2f}")
            else:
                print(f"Aucune moyenne disponible pour la classe {classe}.")

      
        elif choix == "2":
            stats.generer_rapport_pdf()
        elif choix == "0":
            break
        else:
            print("Option invalide.")

def consulter_notes_personnelles(db, utilisateur_id):
    gestion = GestionEtudiants(db)
    gestion.afficher_notes_etudiant(utilisateur_id)

def main():
    print("Bienvenue dans l'application de gestion des étudiants")
    db = get_db_connection()
    auth_service = AuthService(db)

    token = None
    role = None
    utilisateur_id = None

    while True:
        if token is None:
            choix = afficher_menu_principal()
            if choix == "1":
                menu_inscription(auth_service)
            elif choix == "2":
                token, role, utilisateur_id = menu_connexion(auth_service)
            elif choix == "0":
                print("Au revoir!")
                break
            else:
                print("Option invalide.")
        else:
            choix = afficher_menu_connecte(role)

            if role == "admin":
                if choix == "1":
                    print("Gestion des utilisateurs (à implémenter)")
                elif choix == "2":
                    gerer_etudiants(db)
                elif choix == "3":
                    menu_statistiques(db)
                elif choix == "4":
                    print("Mon profil (à implémenter)")
                elif choix == "5":
                    auth_service.logout(token)
                    token = None
                    role = None
                    utilisateur_id = None
                    print("Déconnexion réussie.")
                elif choix == "0":
                    print("Au revoir!")
                    break
                else:
                    print("Option invalide.")

            elif role == "enseignant":
                if choix == "1":
                    gerer_etudiants(db, utilisateur_id, role)
                elif choix == "2":
                    print("Mon profil (à implémenter)")
                elif choix == "3":
                    auth_service.logout(token)
                    token = None
                    role = None
                    utilisateur_id = None
                    print("Déconnexion réussie.")
                elif choix == "0":
                    print("Au revoir!")
                    break
                else:
                    print("Option invalide.")

            elif role == "etudiant":
                if choix == "1":
                    consulter_notes_personnelles(db, utilisateur_id)
                elif choix == "2":
                    print("Mon profil (à implémenter)")
                elif choix == "3":
                    auth_service.logout(token)
                    token = None
                    role = None
                    utilisateur_id = None
                    print("Déconnexion réussie.")
                elif choix == "0":
                    print("Au revoir!")
                    break
                else:
                    print("Option invalide.")

if __name__ == "__main__":
    main()
