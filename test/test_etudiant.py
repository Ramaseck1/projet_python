import unittest
from models.etudiant import Etudiant

class TestEtudiant(unittest.TestCase):
    def test_moyenne(self):
        etudiant = Etudiant("Rama", "seck", "0600000000", "Terminale", 15)
        self.assertEqual(etudiant.moyenne, 15)

if __name__ == "__main__":
    unittest.main()