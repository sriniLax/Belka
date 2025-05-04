from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
  
  ext_modules = cythonize(["preprocess_data.pyx","Needed_Functions/utils.pyx"]),
  include_dirs=[numpy.get_include()]
  
)