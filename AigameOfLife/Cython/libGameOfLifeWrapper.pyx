cimport numpy as np
import numpy as pnp
from libc.stdlib cimport malloc, free

np.import_array()

cdef extern from "gameOfLife.h":
  struct matchField:
    int xSize, ySize
    int simpleComplexity
    np.uint8_t *fieldMatrixNeighbourCount
    np.uint8_t *fieldMatrix
  void initMatchField(matchField *field)
  void printMatchField(matchField *field)
  void zeroMatchField(matchField *field)
  void resetGame(matchField *field)
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
    # when replacing the C fieldMatrix pointer the old array is replaced and the old one freed before
    def __get__(self):
      cdef np.npy_intp dims[2]
      dims[0] = self.mf.xSize
      dims[1] = self.mf.ySize
      cdef np.ndarray[dtype=np.uint8_t, ndim=2] pyMF = np.PyArray_SimpleNewFromData(2, &dims[0], np.NPY_UINT8, self.mf.fieldMatrix)
      # for some reason axis are transposed after mem read
      return pnp.transpose(pyMF)
    def __set__(self, arr):
      # !warning! frees & allocates new memory every call
      cdef np.uint8_t[:,:] memView = arr
      cdef np.uint8_t* memViewCArr = <np.uint8_t *>malloc(self.mf.xSize * self.mf.ySize * sizeof(np.uint8_t))
      if not memViewCArr: raise MemoryError
      for j in range(self.mf.xSize):
        for i in range(self.mf.ySize):
            memViewCArr[j+self.mf.ySize*i] = memView[j][i]

      free(self.mf.fieldMatrix)
      self.mf.fieldMatrix = &memViewCArr[0]


  property simpleComplexity:
    def __get__(self):
      return self.mf.simpleComplexity
    def __set__(self, simpleComplexity):
      self.mf.simpleComplexity = simpleComplexity

  def __exit__(self):
    freeMatchField(&self.mf)

  def initMatchFieldPy(self):
    initMatchField(&self.mf)

  def printMatchFieldPy(self):
    printMatchField(&self.mf)

  def resetGamePy(self):
    resetGame(&self.mf)

  def zeroMatchFieldPy(self):
    zeroMatchField(&self.mf)

  def setMatchFieldXYpy(self, x, y, val):
    setMatchFieldXY(&self.mf, x, y, val)

  def applyIterationPy(self):
    applyIteration(&self.mf)
