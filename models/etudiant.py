class Etudiant:
    def __init__(self, nom, prenom, telephone, classe, moyenne):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.classe = classe
        self.moyenne = moyenne
    
    def to_dict(self):
        return self.__dict__
