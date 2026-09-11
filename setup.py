import importlib.util
import shutil
import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import setuptools

_ROOT = Path(__file__).resolve().parent


def _load_jar_module():
    spec = importlib.util.spec_from_file_location(
        "pyopsin_jar", _ROOT / "pyopsin" / "jar.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _install_opsin_jar(install_lib=None):
    jar = _load_jar_module()
    try:
        cached = jar.ensure_opsin_jar(force=True)
    except FileNotFoundError as exc:
        print(
            f"Warning: could not download the latest OPSIN JAR during install: {exc}\n"
            "PyOpsin will retry on first use.",
            file=sys.stderr,
        )
        return
    if not install_lib:
        return
    dest = Path(install_lib) / "pyopsin" / jar.JAR_FILENAME
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if cached.resolve() != dest.resolve():
            shutil.copy2(cached, dest)
    except OSError as exc:
        print(
            f"Warning: could not copy OPSIN JAR into {dest}: {exc}",
            file=sys.stderr,
        )


class InstallWithJar(install):
    def run(self):
        super().run()
        _install_opsin_jar(self.install_lib)


class DevelopWithJar(develop):
    def run(self):
        super().run()
        _install_opsin_jar(_ROOT)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyopsin',
    version='0.2.4',
    author='Dingyun Huang',
    author_email='dh582@cam.ac.uk',
    description='A simple python wrapper for OPSIN: Open Parser for Systematic IUPAC nomenclature.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dingyun-Huang/pyopsin",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'jpype1>=1.2.0',
    ],
    cmdclass={
        'install': InstallWithJar,
        'develop': DevelopWithJar,
    },
    entry_points={
        'console_scripts': [
            'PyOPSIN = PyOPSIN.__main__:main',
        ],
    },
)
