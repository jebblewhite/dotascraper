from setuptools import setup
from setuptools import find_packages

setup(
    name='dotascraper', ## This will be the name your package will be published with
    version='0.0.4', 
    description='Package that extracts data from OpenDota to analyse picks/bans and winrates',
    url='https://github.com/jebblewhite/dotascraper.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Jason Ebblewhite', # Your name
    license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['selenium', 'pandas', 'sqlalchemy', 'psycopg2-binary'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)