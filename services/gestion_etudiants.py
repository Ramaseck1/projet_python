# services/gestion_etudiants.py
from models.etudiant import Etudiant
import pandas as pd
from fpdf import FPDF
from Database.mongodb import MongoDBService
from Database.redis import SimpleSessionManager

class GestionEtudiants:
    def __init__(self):
        # Utiliser nos nouveaux services
        mongodb_service = MongoDBService()
        self.collection = mongodb_service.get_collection()
        self.cache = SimpleSessionManager()
        
    def ajouter_etudiant(self, etudiant):
        # Vérification du téléphone unique
        if self.collection.find_one({"telephone": etudiant.telephone}):
            print("Erreur : Le téléphone existe déjà.")
            return

        # Vérification des notes
        if hasattr(etudiant, 'notes') and any(note < 0 or note > 20 for note in etudiant.notes):
            print("Erreur : Les notes doivent être entre 0 et 20.")
            return

        # Conversion de l'étudiant en dictionnaire pour MongoDB
        etudiant_dict = etudiant.to_dict() if hasattr(etudiant, 'to_dict') else {
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "telephone": etudiant.telephone,
            "classe": etudiant.classe,
            "notes": getattr(etudiant, 'notes', []),
            "moyenne": getattr(etudiant, 'moyenne', 0)
        }

        self.collection.insert_one(etudiant_dict)
        self.cache.set(f"etudiant:{etudiant.nom}", str(etudiant_dict))
        print("Étudiant ajouté avec succès.")

    def rechercher_etudiant(self, nom):
        etudiant_cache = self.cache.get(f"etudiant:{nom}")
        if etudiant_cache:
            try:
                return eval(etudiant_cache)
            except (SyntaxError, TypeError):
                # Si le cache n'est pas évaluable
                pass

        etudiant = self.collection.find_one({"nom": nom})
        if etudiant:
            self.cache.set(f"etudiant:{nom}", str(etudiant))
            return etudiant
        return None

    def afficher_etudiants(self):
        etudiants_cache = self.cache.get("etudiants")
        if etudiants_cache:
            try:
                etudiants = eval(etudiants_cache)
            except (SyntaxError, TypeError):
                etudiants = list(self.collection.find())
        else:
            etudiants = list(self.collection.find())
            self.cache.set("etudiants", str(etudiants))

        if not etudiants:
            print("Aucun étudiant trouvé.")
            return

        for etudiant in etudiants:
            print(f"Nom: {etudiant.get('nom')}, Prénom: {etudiant.get('prenom')}, "
                  f"Classe: {etudiant.get('classe')}, Téléphone: {etudiant.get('telephone')}")

    def trier_par_moyenne(self):
        etudiants = list(self.collection.find())
        
        if not etudiants:
            print("Aucun étudiant trouvé.")
            return
            
        for etudiant in etudiants:
            if 'notes' in etudiant and len(etudiant['notes']) > 0:
                etudiant['moyenne_calculee'] = sum(etudiant['notes']) / len(etudiant['notes'])
            else:
                etudiant['moyenne_calculee'] = 0
        
        etudiants.sort(key=lambda e: e['moyenne_calculee'], reverse=True)
        
        for etudiant in etudiants:
            print(f"Nom: {etudiant.get('nom')}, Prénom: {etudiant.get('prenom')}, "
                  f"Classe: {etudiant.get('classe')}, Moyenne: {etudiant.get('moyenne_calculee', 0):.2f}")

    def modifier_notes(self, telephone, nouvelles_notes):
        if any(note < 0 or note > 20 for note in nouvelles_notes):
            print("Erreur : Les notes doivent être entre 0 et 20.")
            return

        result = self.collection.update_one(
            {"telephone": telephone},
            {"$set": {"notes": nouvelles_notes}}
        )
        if result.modified_count:
            etudiant = self.collection.find_one({"telephone": telephone})
            self.cache.set(f"etudiant:{etudiant['nom']}", str(etudiant))
            # Calculer et mettre à jour la moyenne
            if len(nouvelles_notes) > 0:
                moyenne = sum(nouvelles_notes) / len(nouvelles_notes)
                self.collection.update_one(
                    {"telephone": telephone},
                    {"$set": {"moyenne": moyenne}}
                )
            print("Notes mises à jour avec succès.")
        else:
            print("Étudiant non trouvé.")

    def supprimer_etudiant(self, telephone):
        etudiant = self.collection.find_one({"telephone": telephone})
        if etudiant:
            self.collection.delete_one({"telephone": telephone})
            self.cache.delete(f"etudiant:{etudiant['nom']}")
            print("Étudiant supprimé.")
        else:
            print("Étudiant non trouvé.")

    def exporter_donnees(self, format):
        etudiants = list(self.collection.find())
        if not etudiants:
            print("Aucune donnée à exporter.")
            return
            
        # Supprimer l'ID MongoDB pour l'exportation
        for e in etudiants:
            if '_id' in e:
                del e['_id']
                
        df = pd.DataFrame(etudiants)

        if format == "csv":
            df.to_csv("etudiants.csv", index=False)
            print("Exportation CSV réussie: etudiants.csv")
        elif format == "json":
            df.to_json("etudiants.json", orient="records")
            print("Exportation JSON réussie: etudiants.json")
        elif format == "excel":
            df.to_excel("etudiants.xlsx", index=False)
            print("Exportation Excel réussie: etudiants.xlsx")
        elif format == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # En-têtes
            colonnes = df.columns
            for col in colonnes:
                pdf.cell(40, 10, col, 1)
            pdf.ln()
            
            # Données
            for _, row in df.iterrows():
                for col in colonnes:
                    valeur = str(row[col])
                    # Limiter la longueur des cellules
                    if len(valeur) > 30:
                        valeur = valeur[:27] + "..."
                    pdf.cell(40, 10, valeur, 1)
                pdf.ln()
                
            pdf.output("etudiants.pdf")
            print("Exportation PDF réussie: etudiants.pdf")
        else:
            print("Format non pris en charge.")


    
    def moyenne_generale_classe(self, classe):
        etudiants = list(self.collection.find({"classe": classe}))

        if not etudiants:
            print(f"Aucun étudiant trouvé pour la classe {classe}.")
            return 0

        total_moyenne = 0
        compteur = 0

        for e in etudiants:
            if "notes" in e and isinstance(e["notes"], list) and e["notes"]:
                moyenne = sum(e["notes"]) / len(e["notes"])
                total_moyenne += moyenne
                compteur += 1

        if compteur == 0:
            return 0

        return total_moyenne / compteur

    def importer_donnees(self, fichier):
        try:
            if fichier.endswith(".csv"):
                df = pd.read_csv(fichier)
            elif fichier.endswith(".xlsx"):
                df = pd.read_excel(fichier)
            else:
                print("Format non supporté. Utilisez CSV ou Excel.")
                return
                
            compteur = 0
            for _, row in df.iterrows():
                try:
                    # Gestion des notes (pourraient être stockées sous forme de chaîne ou de liste)
                    notes_brutes = row.get("notes", "[]")
                    if isinstance(notes_brutes, str):
                        try:
                            notes = eval(notes_brutes)
                        except:
                            notes = []
                    else:
                        notes = notes_brutes
                        
                    from models.etudiant import Etudiant
                    etudiant = Etudiant(
                        nom=row["nom"],
                        prenom=row["prenom"],
                        telephone=row["telephone"],
                        classe=row["classe"],
                        notes=notes
                    )
                    self.ajouter_etudiant(etudiant)
                    compteur += 1
                except Exception as e:
                    print(f"Erreur lors de l'importation d'une ligne: {e}")
                    
            print(f"{compteur} étudiants importés avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'importation du fichier: {e}")

    def recherche_multi_critere(self, critere, valeur):
        # Convertir en nombre si nécessaire
        if critere in ["moyenne", "notes"]:
            try:
                valeur = float(valeur)
            except:
                pass
                
        etudiants = list(self.collection.find({critere: valeur}))
        
        if not etudiants:
            print(f"Aucun étudiant trouvé avec {critere} = {valeur}")
            return
            
        print(f"Résultats pour {critere} = {valeur}:")
        for e in etudiants:
            print(f"Nom: {e.get('nom')}, Prénom: {e.get('prenom')}, "
                  f"Classe: {e.get('classe')}, Téléphone: {e.get('telephone')}")