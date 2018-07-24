__author__ = "Daniel Castelli"
from setuptools import setup
from setuptools.command.install import install as _install
import subprocess

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        subprocess.call("msiexec /i pytic\\drivers\\pololu-tic-1.6.2-win.msi")

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

setup(
    name = "PyTic",
    version = "0.0.2",
    author = "Daniel Castelli",
    #email = "",
    description = "An object-oriented Python wrapper for Pololu Tic Stepper Controllers.",
    license = "MIT",
    keywords = "PyTic Pololu Tic Stepper Controller Wrapper",
    # url = "",
    packages = ['pytic'],
    install_requires = ['PyYAML'],
    include_package_data=True,
    cmdclass = {'install': install},
)