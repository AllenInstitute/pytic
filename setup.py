__author__ = "Daniel Castelli"
from setuptools import setup

setup(
    name = "PyTic",
    version = "0.0.1",
    author = "Daniel Castelli",
    #email = "",
    description = "An object-oriented Python wrapper for Pololu Tic Stepper Controllers.",
    license = "MIT",
    keywords = "PyTic Pololu Tic Stepper Controller Wrapper",
    # url = "",
    packages = ['pytic'],
    install_requires = ['PyYAML'],
    include_package_data=True,
)