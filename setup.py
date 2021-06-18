from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name = "ccs2",
    packages=['ccs2', 'ccs2.generate_code', 'ccs2.lexical', 'ccs2.syntax', 'ccs2.semantic', 'ccs2.utils'],
    entry_points = {
        "console_scripts": ['ccs2 = ccs2.compile:Compile']
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    version = '1.0.0',
    description = "C Compiler Simulator",
    author = "Umberto Barros",
    license = 'MIT'
)