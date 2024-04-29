PyOPSIN
====================

This is a Python wrapper for the OPSIN (Open Parser for Systematic IUPAC Nomenclature) package, which allows you to generate SMILES and CML form the standardized IUPAC names for organic molecules. The original OPSIN package was written in Java, but this wrapper allows you to use OPSIN functionality directly from Python.

Installation
------------

To install PyOPSIN, clone the repository and run
```
pip install -e .
```
Usage
-----

Here's an example of how to use the PyOPSIN to generate an IUPAC name for a molecule:
```python
from pyopsin import PyOpsin

# create an PyOpsin object
opsin = PyOpsin()

# generate the SMILES string from an IUPAC name for a molecule
name = "2,4,6-trinitrotoluene"
smiles = pyopsin.to_smiles(name)

# print the IUPAC name
print(smiles)
```
This should output the following IUPAC name:
```
[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]
```

Acknowledgments
---------------

The OPSIN Python wrapper is built on top of the [OPSIN package](https://opsin.ch.cam.ac.uk/), which was developed by the Centre for Molecular Informatics at the University of Cambridge. We would like to thank the developers of OPSIN for creating such a powerful and useful tool.
