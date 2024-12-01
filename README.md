PyOPSIN
====================

This is a Python wrapper for the OPSIN (Open Parser for Systematic IUPAC Nomenclature) package, which allows you to generate SMILES and CML form the standardized IUPAC names for organic molecules. The original OPSIN package was written in Java, but this wrapper allows you to use OPSIN functionality directly from Python.

Installation
------------

To install PyOPSIN, run

```bash
pip install pyopsin
```

Usage
-----

Here's an example of how to use the PyOPSIN to generate SMILES string using the IUPAC name for a molecule:

```python
from pyopsin.pyopsin import PyOpsin

# create an PyOpsin object
opsin = PyOpsin()

# generate the SMILES string from an IUPAC name for a molecule
name = "2,4,6-trinitrotoluene"
smiles = pyopsin.to_smiles(name)

# print the SMILES string
print(smiles)
```

This should output the following SMILES string:

```bash
[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]
```

Here is another example of how to invoke parallel processing to process a list of IUPAC names:

```python
names = ["2,4,6-trinitrotoluene", "cycloheptene"]
smiles = pyopsin.to_smiles(names, num_workers=2)
print(smiles)
```

This should output the following SMILES strings:

```bash
["[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]", "C1=CCCCCC1"]
```

Acknowledgments
---------------

The OPSIN Python wrapper is built on top of the [OPSIN package](https://opsin.ch.cam.ac.uk/), which was developed by the Centre for Molecular Informatics at the University of Cambridge. We would like to thank the developers of OPSIN for creating such a powerful and useful tool.
