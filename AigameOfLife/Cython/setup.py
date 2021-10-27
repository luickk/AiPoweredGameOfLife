from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

libGameOfLifeWrapper = Extension(
    name="gameOfLife",
    sources=["libGameOfLifeWrapper.pyx"],
    libraries=["GameOfLife"],
    library_dirs=["../../libGameOfLife/build/src/"],
    include_dirs=["../../libGameOfLife/src/", numpy.get_include()]
)
setup(
    name="gameOfLife",
    ext_modules=cythonize([libGameOfLifeWrapper])
)
