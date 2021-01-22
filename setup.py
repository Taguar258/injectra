import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="injectra",
    description="Injectra injects shellcode payloads into mac OSX applications.",
    long_description=read("README.md"),
    author="Taguar258",
    license="MIT",
    version="2.0",
    keywords="macos osx backdoor virus injection trojan rat injector payload",
    url="https://github.com/Taguar258/injectra",
    entry_points={"console_scripts": ["injectra = injectra.injectra:exec_main"]},
    package_dir={"injectra": "injectra"},
    packages=["injectra", "injectra.src"],
    classifiers=["License :: OSI Approved :: MIT License"],
)
