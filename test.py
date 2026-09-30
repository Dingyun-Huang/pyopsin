import unittest

from pyopsin.pyopsin import PyOpsin


class TestPyOpsinClean(unittest.TestCase):
    def setUp(self):
        self.pyopsin = PyOpsin()
        self.names = ["2,4,6-trinitrotoluene", "cycloheptene"]

    def test_to_smiles_single(self):
        smiles = self.pyopsin.to_smiles_single(self.names[0])
        self.assertEqual(
            smiles, "[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]"
        )

    def test_to_smiles(self):
        smiles = self.pyopsin.to_smiles(self.names, num_workers=2)
        self.assertCountEqual(
            smiles,
            ["[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]", "C1=CCCCCC1"],
        )


class TestPyOpsinAmbiguous(unittest.TestCase):
    def setUp(self) -> None:
        self.pyopsin = PyOpsin(capture_message=True)
        self.names = ["dichlorobenze", "dichlorobenzene"]
        self.answers = [
            {
                "chemical_name": "dichlorobenze",
                "smiles": None,
                "message": "dichlorobenze is unparsable due to the following being uninterpretable: benze The following was not parseable: e",
                "status": "FAILURE",
            },
            {
                "chemical_name": "dichlorobenzene",
                "smiles": "ClC1=C(C=CC=C1)Cl",
                "message": "APPEARS_AMBIGUOUS: Connection of chloro to benzen",
                "status": "WARNING",
            },
        ]
        return super().setUp()

    def test_to_smiles_single_wrong(self):
        out = self.pyopsin.to_smiles_single(self.names[0])
        self.assertDictEqual(
            out,
            self.answers[0],
        )

    def test_to_smiles_single_ambiguous(self):
        out = self.pyopsin.to_smiles_single(self.names[1])
        self.assertDictEqual(
            out,
            self.answers[1],
        )

    def test_to_smiles(self):
        out = self.pyopsin.to_smiles(self.names, num_workers=2)
        self.assertListEqual(out, self.answers)


if __name__ == "__main__":
    unittest.main()
