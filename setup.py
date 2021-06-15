from setuptools import setup, find_packages


setup(
    name='lyrics',
    version='1.0.0',
    install_requires=[
        'flask',
        'flask-cors',
        'bs4',
        'requests'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ]
    }
)
