"""
Setup.py maintained for legacy systems
"""

from setuptools import setup, find_packages


setup(
    name="newstore_connector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'api_toolkit',
        'requests'
    ],
    dependency_links=[
        'git+https://github.com/kyleranous/api_toolkit.git@main#egg=api_toolkit'
    ]
)
