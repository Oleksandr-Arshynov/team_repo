from setuptools import setup, find_packages

setup(
    name='assistant',
    version='0.1',
    packages=find_packages(),
    description='Assistant package',
    long_description='Your long description here.',
    long_description_content_type='text/x-rst',
    install_requires=[
        'rich',
        'prompt_toolkit',
        'python-dateutil',
    ],
)
