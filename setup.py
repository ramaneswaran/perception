from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()
package_dir = here / "perception"

# Packages required for this module to be executed
def list_reqs(fname="requirements.txt"):
    with open(fname) as fd:
        return fd.read().splitlines()


# Get the long description from the README file
long_description = open(here / "README.md").read()

# Version
version = open(package_dir / "VERSION").read().strip()

setup(
    name="perception",
    version=version,
    description="Automatic food recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramaneswaran/perception",
    author="Ramaneswaran",
    packages=find_packages(exclude=("tests")),
    package_data={"perception": ["VERSION"]},
    include_package_data=True,
    license="License :: OSI Approved :: MIT License",
    install_requires=list_reqs(),
    extras_requre=["pytest", "black", "flake8"],
    keywords=["machine learning", "benchmark", "pmlb"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
)