from setuptools import setup, find_packages

setup(
    name='main',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'rich',
        'prompt_toolkit',
        'tabulate',
    ],
)
