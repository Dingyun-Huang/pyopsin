import unittest
from pyopsin.pyopsin import PyOpsin

class TestPyOpsin(unittest.TestCase):
    def setUp(self):
        self.pyopsin = PyOpsin()
        self.names = ["2,4,6-trinitrotoluene", "cycloheptene"]

    def test_to_smiles_single(self):
        smiles = self.pyopsin.to_smiles_single(self.name[0])
        self.assertEqual(smiles, "[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]")
    
    def test_to_smiles(self):
        smiles = self.pyopsin.to_smiles(self.names)
        self.assertCountEqual(smiles, ["[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]", "C1=CCCCCC1"])


if __name__ == '__main__':
    unittest.main()