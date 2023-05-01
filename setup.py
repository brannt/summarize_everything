#!/usr/bin/env python
# This setup.py is here only because pip doesn't support editable mode for pyproject.toml yet

from setuptools import setup, find_packages

try:
    from summarizer import __version__
except ImportError:
    __version__ = "unknown"

def read_requirements(name="main"):
    with open(f"requirements/{name}.txt") as f:
        return f.read().splitlines()

setup(
    name="summarize_everything",
    version=__version__,
    description="summarize_everything package",
    author="Artem Gorokhov",
    author_email="branntart@gmail.com",
    packages=find_packages(),
    install_requires=read_requirements(),
    extras_require={
        "dev": read_requirements("dev"),
        "telegram": read_requirements("telegram"),
    }
)