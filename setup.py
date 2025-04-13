from setuptools import setup, find_packages

setup(
    name="dmforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "dmforge=main:app",
        ],
    },
)
