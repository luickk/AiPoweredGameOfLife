#include <stdint.h>

typedef struct {
  int xSize, ySize;

  // using int for the sake of simplicity TODO: change to bitmask (don't know whether it's even worth the extra computing time)
  int **fieldMatrix;
} matchField;

typedef struct twoDimCords {
  int x, y;
} fieldCords;

// internal
int fieldBoundaryCheck(matchField *field, fieldCords *cords);

void getNneighbours(matchField *field, fieldCords *cords, int *nNeighbours);

// lib
void printMatchField(matchField *field);

void zeroMatchField(matchField *field);

void initMatchField(matchField *field);

void freeMatchField(matchField *field);

void applyIteration(matchField *field);
