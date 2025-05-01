
from Database.mongodb import get_mongo_collection
from models.etudiant import Etudiant
class GestionEtudiants:
    def __init__(self):
        self.collection =  get_mongo_collection()

    def ajouter_etudiant(self, etudiant: Etudiant):
        # Vérification du téléphone unique
        if self.collection.find_one({"telephone": etudiant.telephone}):
            print("Erreur : Le téléphone existe déjà.")
            return

        # Vérification des notes
        if any(note < 0 or note > 20 for note in etudiant.notes):
            print("Erreur : Les notes doivent être entre 0 et 20.")
            return

        self.collection.insert_one(etudiant.to_dict())
        self.cache.set(f"etudiant:{etudiant.nom}", str(etudiant.to_dict()))
        print("Étudiant ajouté avec succès.")

    def rechercher_etudiant(self, nom):
        etudiant_cache = self.cache.get(f"etudiant:{nom}")
        if etudiant_cache:
            return eval(etudiant_cache)

        etudiant = self.collection.find_one({"nom": nom})
        if etudiant:
            self.cache.set(f"etudiant:{nom}", str(etudiant))
            return etudiant
        return None

    def afficher_etudiants(self):
        etudiants_cache = self.cache.get("etudiants")
        if etudiants_cache:
            etudiants = eval(etudiants_cache)
        else:
            etudiants = list(self.collection.find())
            self.cache.set("etudiants", str(etudiants))

        for etudiant in etudiants:
            print(etudiant)

    def trier_par_moyenne(self):
        etudiants = list(self.collection.find())
        etudiants.sort(key=lambda e: sum(e['notes']) / len(e['notes']), reverse=True)
        for etudiant in etudiants:
            print(etudiant)

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
        import pandas as pd
        from fpdf import FPDF

        etudiants = list(self.collection.find())
        df = pd.DataFrame(etudiants)

        if format == "csv":
            df.to_csv("etudiants.csv", index=False)
        elif format == "json":
            df.to_json("etudiants.json", orient="records")
        elif format == "excel":
            df.to_excel("etudiants.xlsx", index=False)
        elif format == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for index, row in df.iterrows():
                pdf.cell(200, 10, txt=str(row.to_dict()), ln=True)
            pdf.output("etudiants.pdf")
        else:
            print("Format non pris en charge.")

    def importer_donnees(self, fichier):
        import pandas as pd
        if fichier.endswith(".csv"):
            df = pd.read_csv(fichier)
        elif fichier.endswith(".xlsx"):
            df = pd.read_excel(fichier)
        else:
            print("Format non supporté.")
            return

        for _, row in df.iterrows():
            etudiant = Etudiant(
                nom=row["nom"],
                prenom=row["prenom"],
                telephone=row["telephone"],
                classe=row["classe"],
                notes=row["notes"] if isinstance(row["notes"], list) else eval(row["notes"])
            )
            self.ajouter_etudiant(etudiant)

    def recherche_multi_critere(self, critere, valeur):
        etudiants = list(self.collection.find({critere: valeur}))
        for e in etudiants:
            print(e)
