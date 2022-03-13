from setuptools import find_packages, setup

setup(
    name='ml-assignment',
    version='0.1.0',
    packages=find_packages(include=['main', 'main.*']),
    install_requires=[
        'PyYAML',
        'pandas',
        'numpy',
        'matplotlib',
        'plotly',
        'jupyter',
        'dash',
        'dash_bootstrap_components',
        'flask_caching',
        'randomname',
        'pymongo[srv]',
        'flask_pymongo',
        'sklearn',
        'spacy'
    ]
)