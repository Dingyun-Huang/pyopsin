PyOPSIN
====================

This is a Python wrapper for the OPSIN (Open Parser for Systematic IUPAC Nomenclature) package, which allows you to generate SMILES and CML form the standardized IUPAC names for organic molecules. The original OPSIN package was written in Java, but this wrapper allows you to use OPSIN functionality directly from Python.

Installation
------------

PyOPSIN requires **Java 8+**. The first time you create a `PyOpsin()` instance, it downloads the latest OPSIN CLI JAR (`opsin-cli-*-jar-with-dependencies.jar`) from the [official OPSIN GitHub releases](https://github.com/dan2097/opsin/releases).

```bash
pip install pyopsin
```

From a source checkout:

```bash
pip install -e .
```

The JAR is cached under `~/.cache/pyopsin/` on Unix and `%LOCALAPPDATA%\pyopsin` on Windows. Override the cache directory with the `PYOPSIN_JAR_DIR` environment variable. You can also pass a local JAR with `PyOpsin(path="/path/to/opsin-cli.jar")`.

Usage
-----

Here's an example of how to use the PyOPSIN to generate SMILES string using the IUPAC name for a molecule:

```python
from pyopsin import PyOpsin

# create an PyOpsin object
opsin = PyOpsin()

# generate the SMILES string from an IUPAC name for a molecule
name = "2,4,6-trinitrotoluene"
smiles = opsin.to_smiles(name)

# print the SMILES string
print(smiles)
```

This should output the following SMILES string:

```bash
["[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]"]
```

Here is another example of how to invoke parallel processing to process a list of IUPAC names:

```python
names = ["2,4,6-trinitrotoluene", "cycloheptene"]
smiles = opsin.to_smiles(names, num_workers=2)
print(smiles)
```

This should output the following SMILES strings:

```bash
["[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]", "C1=CCCCCC1"]
```

With the default `capture_message=False`, `to_smiles` returns a list of SMILES strings. Pass `capture_message=True` to include the OPSIN parse status and message for each name. Each result is a dictionary with these keys:

- `chemical_name`: the input IUPAC name
- `smiles`: the SMILES string, or `None` when parsing fails
- `message`: the OPSIN message
- `status`: the OPSIN status name, such as `SUCCESS`, `WARNING`, or `FAILURE`

```python
opsin = PyOpsin(capture_message=True)

names = ["dichlorobenze", "dichlorobenzene"]
results = opsin.to_smiles(names)
print(results)
```

This should output:

```python
[
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
```

`to_smiles_single` returns the same dictionary for one name.

Tests
-----

```bash
python -m unittest test.py
```

`TestPyOpsinClean` checks SMILES conversion for valid names. `TestPyOpsinAmbiguous` checks `capture_message=True` for an unparsable name (`FAILURE`) and an ambiguous name (`WARNING`).

Acknowledgments
---------------

The OPSIN Python wrapper is built on top of the [OPSIN package](https://opsin.ch.cam.ac.uk/), which was developed by the Centre for Molecular Informatics at the University of Cambridge. We would like to thank the developers of OPSIN for creating such a powerful and useful tool.
