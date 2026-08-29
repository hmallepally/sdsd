from setuptools import setup, find_packages

setup(
    name="sdsd",
    version="1.0.0",
    py_modules=["sdsd"],
    install_requires=[
        "pydantic>=2.0.0",
        "pytest>=7.0.0",
        "hypothesis>=6.80.0",
    ],
    entry_points={
        "console_scripts": [
            "sdsd=sdsd:main",
        ],
    },
)
