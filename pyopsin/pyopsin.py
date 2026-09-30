from __future__ import annotations

from multiprocessing.pool import ThreadPool

import jpype
import jpype.imports
from jpype.types import *

from .jar import resolve_opsin_jar


class PyOpsin:
    """Class for initializing JAVA virtual machine in Python and OPSIN.
    """

    def __init__(self, path: str | None = None,
                 exit_on_error: bool = False,
                 capture_message: bool = False,
                 allowUninterpretableStereo: bool = False,
                 allowRadicals: bool = False,
                 wildcardRadicals: bool = False,
                 allowAcidsWithoutAcid: bool = False,
                 ):
        """

        Args:
            path (str, Optional): absolute path of the opsin cli .jar file. Defaults to a packaged, cached, or newly downloaded JAR.
            exit_on_error: (bool, optional) break from all parsing when one python process fails, default True
            capture_message: (bool, optional) return a list of dictionaries that capture opsin message, default False
            allowUninterpretableStereo (bool, optional): Defaults to False.
            allowRadicals (bool, optional): Defaults to False.
            wildcardRadicals (bool, optional): Defaults to False.
            allowAcidsWithoutAcid (bool, optional): Defaults to False.

        Raises:
            FileNotFoundError: No opsin cli .jar file was found.
        """
        
        self.exit_on_error = exit_on_error
        self.capture_message = capture_message
        self.path = str(resolve_opsin_jar(path))

        if not jpype.isJVMStarted():
            jpype.startJVM("--enable-native-access=ALL-UNNAMED", classpath=[self.path])
        from uk.ac.cam.ch.wwmm import opsin

        self.config = opsin.NameToStructureConfig()
        if allowUninterpretableStereo:
            self.config.setWarnRatherThanFailOnUninterpretableStereochemistry(
                True)
        if allowRadicals:
            self.config.setAllowRadicals(True)
        if allowAcidsWithoutAcid:
            self.config.setInterpretAcidsWithoutTheWordAcid(True)
        if wildcardRadicals:
            self.config.setOutputRadicalsAsWildCardAtoms(True)

        self.nts = opsin.NameToStructure.getInstance()

    def to_smiles(self, name: str | list[str], num_workers: int = 1) -> list[str] | list[dict]:
        """
        Compute the SMILES strings of a list of molecule IUPAC names in parallel.
        Args:
            name (Union[str, List[str]]): A single IUPAC name or a list of IUPAC names of molecules.
        Returns:
            List[str]: A list of SMILES strings corresponding to the input IUPAC names.
        Raises:
            ValueError: If the input name is not a string or a list of strings.
        """
        if isinstance(name, str):
            return [self.to_smiles_single(name)]
        elif isinstance(name, list):
            if num_workers > 1:
                with ThreadPool(num_workers) as p:
                    return p.map(self.to_smiles_single, name)
            else:
                return [self.to_smiles_single(n) for n in name]
        else:
            raise TypeError(
                "Input name must be a string or a list of strings.")

    def to_smiles_single(self, name: str) -> str | dict:
        """compute a single SMILES of a molecule for its IUPAC name

        Args:
            name (str): IUPAC name of a molecule

        Returns:
            str: SMILES of the molecule
        """
        try:
            results = self.nts.parseChemicalName(name, self.config)
        except Exception as e:
            if self.exit_on_error:
                raise ValueError(f"Failed to parse the name: {name} due to exception {e}") from e
            else:
                print(f"Failed to parse the name: {name} due to exception {e}")
                return None
        smiles = results.getSmiles()
        if self.capture_message:
            message = results.getMessage()
            status = results.getStatus().name()
            return {"chemical_name": name, "smiles": smiles, "message": message, "status": status}
        return str(smiles) if smiles else None

    def to_cml(self, name: str) -> str:
        """compute CML of a molecule from its IUPAC name

        Args:
            name (str): IUPAC name of a molecule

        Returns:
            str: CML of the molecule
        """
        results = self.nts.parseChemicalName(name, self.config)
        return results.getCml()
