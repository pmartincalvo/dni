from setuptools import setup, find_packages
from pathlib import Path
import re

PACKAGE_NAME = "dni"


def get_version():
    version = "unknown"

    version_file_path = Path(PACKAGE_NAME, "_version.py")
    version_file_contents = open(version_file_path, "rt").read()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    a_match = re.search(version_regex, version_file_contents, re.M)
    if a_match:
        version = a_match.group(1)

    return version


setup(
    name=PACKAGE_NAME,
    version=get_version(),
    author="Pablo Martin Calvo",
    author_email="pablomartincalvo+dni@gmail.com",
    packages=find_packages(),
    license="MIT License",
    url="https://github.com/pmartincalvo/dni",
    description="Deal with Spanish DNIs in a Pythonic way.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    project_urls={
        "Documentation": "https://dni.readthedocs.io",
        "Source": "https://github.com/pmartincalvo/dni",
    },
)
