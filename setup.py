"""
Setup script za gradnjo EXE za Windows
Koristi PyInstaller za kreiranje zagonskega programa
"""

from setuptools import setup, find_packages

setup(
    name='DAHUA Camera Discovery',
    version='1.0.0',
    description='DAHUA Camera Discovery Tool - Testiranje in odkrivanje kamer v lokalni mreži',
    author='gregabahun',
    python_requires='>=3.7',
    packages=find_packages(),
    py_modules=['dahua_discovery', 'dahua_discovery_gui'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dahua-discovery=dahua_discovery:main',
        ],
        'gui_scripts': [
            'dahua-discovery-gui=dahua_discovery_gui:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
