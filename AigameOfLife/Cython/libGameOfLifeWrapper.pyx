cimport numpy as np
from libc.stdlib cimport malloc, free

np.import_array()

cdef extern from "gameOfLife.h":
  struct matchField:
    int xSize, ySize
    np.uint8_t **fieldMatrixNeighbourCount
    np.uint8_t **fieldMatrix
  void initMatchField(matchField *field)
  void printMatchField(matchField *field)
  void zeroMatchField(matchField *field)
  void setMatchFieldXY(matchField *field, int x, int y, int val)
  void initMatchField(matchField *field)
  void freeMatchField(matchField *field)
  void applyIteration(matchField *field)

cdef class matchFieldPy:
  cdef matchField mf

  def __init__(self, x, y):
    self.mf.xSize = x;
    self.mf.ySize = y;
    initMatchField(&self.mf)

  property fieldMatrix:
    # memory is then freed by the c freeMatchField at py object free
    def __get__(self):
      cdef np.npy_intp dims[2]
      dims[0] = self.mf.xSize
      dims[1] = self.mf.ySize
      #create a new memory view and PyArray_SimpleNewFromData to deal with the pointer
      cdef np.ndarray[dtype=np.uint8_t, ndim=2] pyMF = np.PyArray_SimpleNewFromData(2, &dims[0], np.NPY_UINT8, self.mf.fieldMatrix)
      return pyMF
    def __set__(self, arr):
      cdef np.npy_intp dims[2]
      dims[0] = self.mf.xSize
      dims[1] = self.mf.ySize
      cdef np.uint8_t[:,:] memView= np.PyArray_SimpleNew(2, &dims[0], arr)
      cdef np.uint8_t** point_to_a = <np.uint8_t **>malloc(self.mf.xSize * sizeof(np.uint8_t*))
      if not point_to_a: raise MemoryError

      for i in range(self.mf.xSize):
          point_to_a[i] = &memView[i, 0]
      self.mf.fieldMatrix = &point_to_a[0]


  def __exit__(self):
    freeMatchField(&self.mf)

  def initMatchFieldPy(self):
    initMatchField(&self.mf)

  def printMatchFieldPy(self):
    printMatchField(&self.mf)

  def zeroMatchFieldPy(self):
    zeroMatchField(&self.mf)

  def setMatchFieldXYpy(self, x, y, val):
    setMatchFieldXY(&self.mf, x, y, val)

  def applyIterationPy(self):
    applyIteration(&self.mf)
