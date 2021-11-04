from setuptools import setup, find_namespace_packages

setup(name="symcollab-xor",
    version="0.2.0",
    packages=find_namespace_packages(include=["symcollab.*"]),
    url="https://github.com/symcollab/cryptosolve",
    install_requires = [
        # Our dependencies
        "symcollab-algebra"
    ],
)
