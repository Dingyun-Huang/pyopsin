import jpype
import jpype.imports
from jpype.types import *

class NameToSmiles:
    
    def __init__(self, path):
        self.path = path

    def name_to_smiles(self, name, allowUninterpretableStereo=False):
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[self.path])
        from uk.ac.cam.ch.wwmm import opsin
        nts = opsin.NameToStructure.getInstance()
        ntsconfig = opsin.NameToStructureConfig()
        if allowUninterpretableStereo:
            ntsconfig.setWarnRatherThanFailOnUninterpretableStereochemistry(True)
        results = nts.parseChemicalName(name, ntsconfig)
        return results.getSmiles()


if __name__ == "__main__":
    pass
    #### example use ####
    # nts = NameToSmiles("E:\PhD\cde_application\pyopsin\opsin_cli.jar")
    # name = "biphenyl"
    # smiles = nts.name_to_smiles(name, allowUninterpretableStereo=True)
    # print(smiles)
