# services/statistiques_service.py

from fpdf import FPDF
from Database.mongodb import get_mongo_collection


class StatistiquesService:
    def __init__(self, db: get_mongo_collection):
        self.db = db
        self.collection = db["etudiants"]

    def moyenne_generale_classe(self, classe):
        etudiants = list(self.collection.find({"classe": classe}))
        
        if not etudiants:
            print("Aucun étudiant trouvé dans cette classe.")
            return None
        
        total = 0
        compteur = 0

        for e in etudiants:
            if 'notes' in e and len(e['notes']) > 0:
                moyenne = sum(e['notes']) / len(e['notes'])
                total += moyenne
                compteur += 1

        if compteur == 0:
            print("Aucun étudiant avec des notes dans cette classe.")
            return None

        moyenne_generale = total / compteur
        print(f"Moyenne générale de la classe {classe} : {moyenne_generale:.2f}")
        return moyenne_generale

    def top_10_etudiants(self):
        etudiants = list(self.collection.find())
        resultats = []

        for etudiant in etudiants:
            if "notes" in etudiant and etudiant["notes"]:
                moyenne = sum(etudiant["notes"]) / len(etudiant["notes"])
                etudiant["moyenne"] = moyenne
                resultats.append(etudiant)

        resultats.sort(key=lambda x: x["moyenne"], reverse=True)
        top_10 = resultats[:10]

        for idx, e in enumerate(top_10, 1):
            print(f"{idx}. {e['nom']} {e['prenom']} - Moyenne: {e['moyenne']:.2f}")

        return top_10

    def generer_rapport_pdf(self, chemin="rapport_etudiants.pdf"):
        top_10 = self.top_10_etudiants()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport des 10 meilleurs étudiants", ln=True, align='C')

        pdf.ln(10)
        for idx, e in enumerate(top_10, 1):
            ligne = f"{idx}. {e['nom']} {e['prenom']} - Classe: {e['classe']} - Moyenne: {e['moyenne']:.2f}"
            pdf.cell(200, 10, txt=ligne, ln=True)

        pdf.output(chemin)
        print(f"Rapport PDF généré : {chemin}")
