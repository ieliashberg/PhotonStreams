from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "find_coinciding",            # Module name to import
        sources=["find_coinciding.pyx"],  # Source file
    )
]

setup(
    name="find_coinciding",
    version="1.0",
    ext_modules=cythonize(extensions),
)

