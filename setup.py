from setuptools import setup, find_packages
from typing import List

E_DOT = '-e .'

def get_requirements(file_path: str)->List[str]:
    '''
    Read the requirements file and return the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        [req.replace("\n'"," ") for req in requirements]

    if E_DOT in requirements:
        requirements.remove(E_DOT)

setup(
    name='mlproject',
    version= '0.0.1',	
    author= 'Gaurav',
    author_email='gaurav1211govindwani@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),	
)