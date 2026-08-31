from setuptools import setup, find_packages

setup(
    name="antigravity-iching-deep-research",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "lunar-python>=1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "iching=engine.cli:main",
        ],
    },
)
