from setuptools import setup
import setuptools

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
    entry_points={
        'console_scripts': [
            'PyOPSIN = PyOPSIN.__main__:main',
        ],
    },
)
