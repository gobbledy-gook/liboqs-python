from setuptools import find_packages, setup

setup(
    packages=find_packages(
        exclude=["tests", "docs", "examples"],
    ),
    install_requires = [
        "mitmproxy==11.0.0"
    ],
)
