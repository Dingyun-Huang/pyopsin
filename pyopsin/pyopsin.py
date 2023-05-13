import jpype
import jpype.imports
from jpype.types import *

class NameToStructure:
    
    def __init__(self, path):
        self.path = path

    def name_to_smiles(self, name):
        jpype.startJVM(classpath=[self.path])
        from uk.ac.cam.ch.wwmm import opsin
        nts = opsin.NameToStructure.getInstance()
        smiles = nts.parseToSmiles(name)
        return smiles


if __name__ == "__main__":
    nts = NameToStructure("/home/dh582/pyopsin/opsin_cli.jar")
    name = "biphenyl"
    smiles = nts.name_to_smiles(name)
    print(smiles)
