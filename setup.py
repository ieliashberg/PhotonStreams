from setuptools import setup, Extension

module = Extension(
    'load_stream_module',       # Module name for import.
    sources=['load_stream_module.c'],  # The C source file.
)

setup(
    name='load_stream_module',
    version='1.0',
    ext_modules=[module]
)
