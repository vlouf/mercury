from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Mercury',
    version='0.1.0',
    description='Retrieves radiosounding data for a specified station (e.g. YPDN for Darwin) at specified dates.',
    long_description=readme,
    author='Valentin Louf',
    author_email='valentin.louf@bom.com.au',
    url='https://github.com/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

