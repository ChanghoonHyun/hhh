from setuptools import setup, find_packages

setup(
    name='hhh',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'flake8',
    ],
    entry_points={
        'console_scripts': [
            'hhh = cli:main',
        ],
    },
)
