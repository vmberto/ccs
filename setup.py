from setuptools import setup, find_packages

 
setup(
    name = "ccs2",
    packages=['ccs2', 'ccs2.generate_code', 'ccs2.lexical', 'ccs2.syntax', 'ccs2.semantic', 'ccs2.utils'],
    entry_points = {
        "console_scripts": ['ccs2 = ccs2.compile:Compile']
    },
    version = '1.2.0',
    description = "C Compiler Simulator",
    author = "Umberto Barros",
    license = 'MIT'
)