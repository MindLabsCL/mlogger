from setuptools import find_packages, setup

setup(
    name='mlogger',
    packages=find_packages(include=['mlogger']),
    version='0.0.1',
    description='Mindlabs logs library',
    author='Me',
    license='Mindlabs license',
    install_requires=['pathlib']
)