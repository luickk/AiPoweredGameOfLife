#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "gameOfLife.h"

void zeroMatchField(struct matchField *field) {
  for (int i = 0; i < field->xSize * field->ySize; i++) {
      field->fieldMatrix[i] = 0;
  }
}

void setMatchFieldXY(struct matchField *field, int x, int y, int val) {
  field->fieldMatrix[x+field->ySize*y] = val;
}

void printMatchField(struct matchField *field) {
  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      printf("%d", field->fieldMatrix[ix+field->ySize*iy]);
    }
    printf("\n");
  }
}

void initMatchField(struct matchField *field) {
  // direct memory layout in order to be compatible with python memory protocols
  field->fieldMatrixNeighbourCount = malloc(field->xSize * field->ySize * sizeof(uint8_t*));
  field->fieldMatrix = malloc(field->xSize * field->ySize * sizeof(uint8_t*));

  zeroMatchField(field);
}

void freeMatchField(struct matchField *field) {
  free(field->fieldMatrixNeighbourCount);
  free(field->fieldMatrix);

  free(field);
}

void resetGame(struct matchField *field) {
  zeroMatchField(field);
  field->simpleComplexity = 0;
  field->entropy = 0;
}

double calcLogWithBase(int *base, int x) {
  return log(x)/log(*base);
}

int countCellsAlive(struct matchField *field) {
  int cellsAlive=0;
  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      if (field->fieldMatrix[ix+field->ySize*iy]) {
        cellsAlive++;
      }
    }
  }
  return cellsAlive;
}

// !needs to be called per iteration!
void calcEntropy(struct matchField *field, int *iteration) {
  field->entropy = (1/(field->xSize*field->ySize)) * calcLogWithBase(iteration, (field->xSize*field->ySize)/countCellsAlive(field));
}

int fieldBoundaryCheck(struct matchField *field, int x, int y) {
  if (field->xSize >= x && field->ySize >= y) {
    return 1;
  }
  return 0;
}

void getNneighbours(struct matchField *field, int x, int y, int *nNeighbours) {
  *nNeighbours = 0;
  if (fieldBoundaryCheck(field, x, y)) {
    *nNeighbours += field->fieldMatrix[(x-1)+field->ySize*y];
    *nNeighbours += field->fieldMatrix[(x+1)+field->ySize*y];
    *nNeighbours += field->fieldMatrix[(x-1)+field->ySize*(y+1)];
    *nNeighbours += field->fieldMatrix[(x+1)+field->ySize*(y+1)];
    *nNeighbours += field->fieldMatrix[(x+1)+field->ySize*(y-1)];
    *nNeighbours += field->fieldMatrix[(x-1)+field->ySize*(y-1)];
    *nNeighbours += field->fieldMatrix[x+field->ySize*(y+1)];
    *nNeighbours += field->fieldMatrix[x+field->ySize*(y-1)];
  }
}

void applyIteration(struct matchField *field) {
  int nNeighbours = 0;

  for (int ix = 1; ix < field->xSize-1; ix++) {
    for (int iy = 1; iy < field->ySize-1; iy++) {
      getNneighbours(field, ix, iy , &nNeighbours);
      field->fieldMatrixNeighbourCount[ix+field->ySize*iy] = nNeighbours;
    }
  }

  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      nNeighbours = field->fieldMatrixNeighbourCount[ix+field->ySize*iy];
      if (nNeighbours == 3) {
        field->fieldMatrix[ix+field->ySize*iy] = 1;
        field->simpleComplexity += 1;
      } else if (nNeighbours < 2) {
        field->fieldMatrix[ix+field->ySize*iy] = 0;
        field->simpleComplexity += 1;
      } else if (nNeighbours > 3) {
        field->fieldMatrix[ix+field->ySize*iy] = 0;
        field->simpleComplexity += 1;
      }
    }
  }
}
