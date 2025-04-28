from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    # Pure C extension for fast file → big-int loading
    Extension(
        name="load_stream_module",
        sources=["load_stream_module.c"],
    ),

    # Cython extension for the correlation logic
    Extension(
        name="find_coinciding",
        sources=["find_coinciding.pyx"],
        language="c++",
        include_dirs=["."],               # so it picks up fast_bitcount.h
        extra_compile_args=["-O3", "-std=c++17"],
    ),
]

setup(
    name="photon_sync",
    version="1.0",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
)
