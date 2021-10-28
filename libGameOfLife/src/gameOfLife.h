#include <stdint.h>

struct matchField{
  int xSize, ySize;

  uint8_t *fieldMatrixNeighbourCount;

  // using int for the sake of simplicity TODO: change to bitmask (don't know whether it's even worth the extra computing time)
  uint8_t *fieldMatrix;
};

// internal
void getNneighbours(struct matchField *field, int x, int y, int *nNeighbours);

int fieldBoundaryCheck(struct matchField *field, int x, int y);

// lib
void printMatchField(struct matchField *field);

void setMatchFieldXY(struct matchField *field, int x, int y, int val);

void zeroMatchField(struct matchField *field);

void initMatchField(struct matchField *field);

void freeMatchField(struct matchField *field);

void applyIteration(struct matchField *field);
