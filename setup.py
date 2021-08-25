import os

from setuptools import find_packages, setup

install_requires = [
    'rasterio>=1.2.6',
    'docker>=5.0.0',
    'matplotlib>=3.4.2',
    'shapely>=1.7.1',
    'numpy>=1.21.1'
]

packages = find_packages()

g = {}
with open(os.path.join('cfactor', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='cfactor',
    version=version,
    description='ToDo',
    license='MIT',
    author='Brazil Data Cube Team',
    author_email='brazildatacube@dpi.inpe.br',
    packages=packages,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
