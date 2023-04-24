import jpype
import jpype.imports
from jpype.types import *

class NameToStructure:
    
    def __init__(self, path):
        self.path = path

    def name_to_smiles(self, name):
        jpype.startJVM()
        return None


if __name__ == "__main__":
    nts = NameToStructure("E:/PhD/cde_application/pyopsin/opsin_cli.jar")
    name = "toluene"
    nts.name_to_smiles(name)
