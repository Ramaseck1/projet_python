import csv

def exporter_etudiants_csv(collection):
    etudiants = collection.find()
    with open("etudiants.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Nom", "Prénom", "Téléphone", "Classe", "Moyenne"])
        for e in etudiants:
            writer.writerow([e["nom"], e["prenom"], e["telephone"], e["classe"], e["moyenne"]])
    print("Exportation réussie.")