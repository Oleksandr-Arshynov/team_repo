from setuptools import setup, find_packages

setup(
    name='assistant',
    version='0.1',
    packages=find_packages(),
    description='Assistant package',
    install_requires=[
        'rich',
        'prompt_toolkit',
        'python-dateutil',
    ],
    entry_points={
        'console_scripts': [
            'assistant=team_repo.assistant:main',
            ]
    }
)



