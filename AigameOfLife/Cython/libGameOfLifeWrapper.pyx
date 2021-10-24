cdef extern from "gameOfLife.h":
  struct matchField:
    int xSize, ySize;
    int **fieldMatrixNeighbourCount;
    int **fieldMatrix;

cdef extern from "gameOfLife.h":
  void initMatchField(matchField *field)
  void printMatchField(matchField *field)
  void zeroMatchField(matchField *field)
  void initMatchField(matchField *field)
  void freeMatchField(matchField *field)
  void applyIteration(matchField *field)
