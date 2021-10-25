cdef extern from "gameOfLife.h":
  struct matchField:
    int xSize, ySize
  void initMatchField(matchField *field)
  void printMatchField(matchField *field)
  void zeroMatchField(matchField *field)
  void initMatchField(matchField *field)
  void freeMatchField(matchField *field)
  void applyIteration(matchField *field)

cdef class matchFieldPy:
  cdef matchField mf

  def __init__(self, x, y):
    initMatchField(&self.mf)
    self.mf.xSize = x;
    self.mf.ySize = y;

  def __exit__(self):
    freeMatchField(&self.mf)

  def initMatchFieldPy(self):
    initMatchField(&self.mf)

  def printMatchFieldPy(self):
    printMatchField(&self.mf)

  def zeroMatchFieldPy(self):
    zeroMatchField(&self.mf)

  def applyIterationPy(self):
    applyIteration(&self.mf)
