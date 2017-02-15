from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Mercury',
    version='0.2.0',
    description='Download radiosounding data.',
    long_description=readme,
    author='Valentin Louf',
    author_email='valentin.louf@bom.gov.au',
    url='https://github.com/vlouf/mercury',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
