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
            'your_script_name=your_package.assistant:main',
            ]
    }
)
