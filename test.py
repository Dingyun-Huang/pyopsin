import unittest
from pyopsin.pyopsin import PyOpsin

class TestPyOpsin(unittest.TestCase):
    def setUp(self):
        self.pyopsin = PyOpsin()
        self.name = "2,4,6-trinitrotoluene"

    def test_to_smiles(self):
        smiles = self.pyopsin.to_smiles(self.name)
        self.assertEqual(str(smiles), "[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]")


if __name__ == '__main__':
    unittest.main()