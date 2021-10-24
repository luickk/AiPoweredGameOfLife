from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

libGameOfLifeWrapper = Extension(
    name="gameOfLife",
    sources=["libGameOfLifeWrapper.pyx"],
    libraries=["GameOfLife"],
    library_dirs=["../../libGameOfLife/build/src/"],
    include_dirs=["../../libGameOfLife/src/"]
)
setup(
    name="gameOfLife",
    ext_modules=cythonize([libGameOfLifeWrapper])
)
