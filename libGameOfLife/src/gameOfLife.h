#include <stdint.h>

typedef struct {
  int xSize, ySize;

  int **fieldMatrixNeighbourCount;

  // using int for the sake of simplicity TODO: change to bitmask (don't know whether it's even worth the extra computing time)
  int **fieldMatrix;
} matchField;

typedef struct twoDimCords {
  int x, y;
} fieldCords;

// internal
void getNneighbours(matchField *field, int x, int y, int *nNeighbours);

int fieldBoundaryCheck(matchField *field, int x, int y);

// lib
void printMatchField(matchField *field);

void zeroMatchField(matchField *field);

void initMatchField(matchField *field);

void freeMatchField(matchField *field);

void applyIteration(matchField *field);
