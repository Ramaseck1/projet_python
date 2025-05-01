# Système de Gestion des Étudiants

## Installation
1. Installer les dépendances :
   ```sh
   pip install -r requirements.txt
   ```
2. Lancer MongoDB et Redis.
3. Exécuter le programme.

## Fonctionnalités
- Gestion des étudiants (ajout, recherche, tri, suppression, modification des notes)

- Authentification et gestion des utilisateurs avec rôles

- Exportation des données en formats CSV, JSON, Excel, PDF

- Importation depuis CSV/Excel

- Statistiques : moyenne générale, top 10

- Génération de rapports PD

# CLasse
* class Etudiant:

   Attributs:
    - nom, prenom, telephone, classe, notes
    - moyenne calculée automatiquement
   Méthodes :
    - calculer_moyenne(): calcule la moyenne des notes
    - to_dict(): convertit l'objet en dictionnaire pour insertion MongoDB



* class Utilisateur:

    Attributs:
    - id, nom, email, mot_de_passe (haché), role
   
   Méthodes :
    - hasher_mot_de_passe(mot_de_passe): hash du mot de passe
    - verifier_mot_de_passe(mot_de_passe): vérifie le mot de passe
    - to_dict(): format MongoDB
    - sauvegarder(db): insère l'utilisateur dans la collection MongoDB


# SERVICE

 * Service GestionEtudiants : class GestionEtudiants:

    Méthodes :
      - ajouter_etudiant(etudiant): vérifie et insère un étudiant

      - rechercher_etudiant(nom): recherche dans Mongo ou le cache

      - afficher_etudiants(): affiche tous les étudiants

      - trier_par_moyenne(): tri des étudiants par moyenne

      - modifier_notes(telephone, nouvelles_notes): met à jour les notes

      - supprimer_etudiant(telephone): supprime un étudiant

      - exporter_donnees(format): exporte vers CSV/JSON/Excel/PDF

      - importer_donnees(fichier): importe depuis un fichier

      - recherche_multi_critere(critere, valeur): recherche selon un champ

  * Service AuthService
      - register(): inscription d’un utilisateur
      - login(): connexion avec vérification du mot de passe et retour du token


# Statistiques

   * StatistiquesService.py

      - Calcul de la moyenne d’une classe
      - Génération de rapports PDF
      - Top 10 des étudiants


# Notification

   * notification_service.py
      - Service pour notifier un utilisateur (email, message, etc.)

# Configuration MongoDB
 - mongodb://localhost:27017/

# Configuration redis

# Dependences

   - pymongo

   - bcrypt

   - uuid

   - pandas

   - fpdf
   - redis
