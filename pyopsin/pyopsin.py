import jpype
import jpype.imports
from jpype.types import *
import os
from pkg_resources import resource_filename

class PyOpsin:
    
    def __init__(self, path: str = None, 
                       allowUninterpretableStereo: bool = False, 
                       allowRadicals: bool = False,
                       wildcardRadicals: bool = False,
                       allowAcidsWithoutAcid: bool = False,):
        """Class for initializing JAVA virtual machine in Python and OPSIN.

        Args:
            path (str, Optional): absolute path of the opsin cli .jar file. Defaults to None.
            allowUninterpretableStereo (bool, optional): Defaults to False.
            allowRadicals (bool, optional): Defaults to False.
            wildcardRadicals (bool, optional): Defaults to False.
            allowAcidsWithoutAcid (bool, optional): Defaults to False.

        Raises:
            FileNotFoundError: No opsin cli .jar file was found.
        """

        if not path:
            path = resource_filename(__name__, "opsin_cli.jar")

        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError(f"No OPSIN .jar file was found at {path}, check your path to the file.")

        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[self.path])
        from uk.ac.cam.ch.wwmm import opsin

        self.config = opsin.NameToStructureConfig()
        if allowUninterpretableStereo:
            self.config.setWarnRatherThanFailOnUninterpretableStereochemistry(True)
        if allowRadicals:
            self.config.setAllowRadicals(True)
        if allowAcidsWithoutAcid:
            self.config.setInterpretAcidsWithoutTheWordAcid(True)
        if wildcardRadicals:
            self.config.setOuputRadicalsAsWildCardAtoms(True)
        
        self.nts = opsin.NameToStructure.getInstance()


    def to_smiles(self, name: str) -> str:
        """compute SMILES of a molecule for its IUPAC name

        Args:
            name (str): IUPAC name of a molecule

        Returns:
            str: SMILES of the molecule
        """

        results = self.nts.parseChemicalName(name, self.config)
        return results.getSmiles()
    
    def to_cml(self, name: str) -> str:
        """compute CML of a molecule from its IUPAC name

        Args:
            name (str): IUPAC name of a molecule

        Returns:
            str: CML of the molecule
        """
        results = self.nts.parseChemicalName(name, self.config)
        return results.getCml()


if __name__ == "__main__":
    pass
    #### example use ####
    """
    pyopsin = PyOpsin()
    name = "2,4,6-trinitrotoluene"
    smiles = pyopsin.to_smiles(name)
    cml = pyopsin.to_cml(name)
    print(smiles)
    print(cml)
    """
