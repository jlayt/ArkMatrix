import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="arkmatrix",
    version="0.1.0",
    url="https://gitlab.com/arklab/ArkMatrix",
    license="GPL3+",
    maintainer="L - P : Archaeology",
    maintainer_email="ark@lparchaeology.com",
    description="A tool for creating and manipulating Harris Matrices.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["networkx", "flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
