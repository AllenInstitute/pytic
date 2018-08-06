__author__ = "Daniel Castelli"
from setuptools import setup
from setuptools.command.install import install as _install
import subprocess

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

setup(
    name = "PyTic",
    version = "0.0.3",
    author = "Daniel Castelli",
    author_email = "danc@alleninstitute.org",
    description = "An object-oriented Python wrapper for Pololu Tic Stepper Controllers.",
    license = "Allen Institute Software License",
    keywords = "PyTic Pololu Tic Stepper Controller Wrapper",
    url = "https://github.com/AllenInstitute/pytic",
    packages = ['pytic'],
    install_requires = ['PyYAML'],
    include_package_data=True,
    cmdclass = {'install': install},
)