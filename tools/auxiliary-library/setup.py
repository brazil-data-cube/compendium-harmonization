import os

from setuptools import find_packages, setup

install_requires = [
    'rasterio>=1.2.6',
    'docker>=5.0.0',
    'matplotlib>=3.4.2',
    'shapely>=1.7.1',
    'numpy>=1.21.1',
    'pandas>='
]

docs_require = [
    'Sphinx>=4.3.0',
    'sphinx-rtd-theme>=1.0.0',
    'sphinxcontrib-napoleon>=0.7'
]

extras_require = {
    'docs': docs_require
}
extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

packages = find_packages()

g = {}
with open(os.path.join('research_processing', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='research-processing',
    version=version,
    description='This library contains the processing and validation methods used in the article: "Evaluating Landsat-8 and Sentinel-2 Nadir BRDF Adjusted Reflectance (NBAR) on South of Brazil through a Reproducible and Replicable environment" to generate Surface Reflectance and NBAR data from Landsat-8 and Sentinel-2 images.',
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
