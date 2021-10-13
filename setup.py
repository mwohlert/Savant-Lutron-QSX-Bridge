"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="Savant-Lutron-QSX-Bridge",  # Required
    version="0.0.1",  # Required
    description="Project to let savant talk to Lutron QSX controller using the LEAP protocol",  # Optional

    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/mwohlert/Savant-Lutron-QSX-Bridge",  # Optional
    author="Tim Lubes & Michel Wohlert",  # Optional
    keywords="savant qsx lutron",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">= 3.3.*",
    install_requires=[
        "cffi==1.14.6",
        "cryptography==35.0.0; python_version >= '3.6'",
        "pycparser==2.20; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
    ],  # Optional
    extras_require={"dev": []},  # Optional
    dependency_links=[
        "git+https://github.com/mwohlert/pylutron-caseta.git@8569b8bf0769cbf02a93964a95c938645cc60e80#egg=pylutron-caseta"
    ],
)
