#include <stdint.h>

typedef struct {
  int xSize, ySize;

  // using int for the sake of simplicity TODO: change to bitmask (don't know whether it's even worth the extra computing time)
  uint8_t **fieldMatrix;
} matchField;

typedef struct twoDimCords {
  int x, y;
} fieldCords;

// internal

int fieldBoundaryCheck(matchField *gameField, fieldCords *cords);

void getNneighbours(matchField *gameField, fieldCords *cords, int *nNeighbours);

// lib

void initMatchField(matchField *gameField);

void freeMatchField(matchField *gameField);

void applyIteration(matchField *gameField);
