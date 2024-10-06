from setuptools import setup, find_packages

setup(
    name="croisslang",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'croisslang=croisslang.cli:main',  # Create 'croisslang' CLI
        ],
    },
    install_requires=[
        # Regular expression library
        "regex==2024.9.11",
        "tqdm==4.66.5"
    ]
)
