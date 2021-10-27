#include <stdio.h>
#include <stdlib.h>

#include "gameOfLife.h"

void zeroMatchField(struct matchField *field) {
  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      field->fieldMatrix[ix][iy] = 0;
    }
  }
}

void setMatchFieldXY(struct matchField *field, int x, int y, int val) {
  field->fieldMatrix[x][y] = val;
}

void printMatchField(struct matchField *field) {
  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      printf("%d", field->fieldMatrix[ix][iy]);
    }
    printf("\n");
  }
}

void initMatchField(struct matchField *field) {
  field->fieldMatrixNeighbourCount = malloc(field->xSize * sizeof(uint8_t*));
  for (int i = 0; i < field->ySize; i++) {
    field->fieldMatrixNeighbourCount[i] = malloc(field->ySize * sizeof(uint8_t));
  }

  field->fieldMatrix = malloc(field->xSize * sizeof(uint8_t*));
  for (int i = 0; i < field->ySize; i++) {
    field->fieldMatrix[i] = malloc(field->ySize * sizeof(uint8_t));
  }
  zeroMatchField(field);
}

void freeMatchField(struct matchField *field) {
  for (int i = 0; i < field->ySize; i++) {
    free(field->fieldMatrixNeighbourCount[i]);
  }
  for (int i = 0; i < field->ySize; i++) {
    free(field->fieldMatrix[i]);
  }
  free(field->fieldMatrixNeighbourCount);
  free(field->fieldMatrix);
  free(field);
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
    *nNeighbours += field->fieldMatrix[x-1][y];
    *nNeighbours += field->fieldMatrix[x+1][y];
    *nNeighbours += field->fieldMatrix[x-1][y+1];
    *nNeighbours += field->fieldMatrix[x+1][y+1];
    *nNeighbours += field->fieldMatrix[x+1][y-1];
    *nNeighbours += field->fieldMatrix[x-1][y-1];
    *nNeighbours += field->fieldMatrix[x][y+1];
    *nNeighbours += field->fieldMatrix[x][y-1];
  }
}

void applyIteration(struct matchField *field) {
  int nNeighbours = 0;

  for (int ix = 1; ix < field->xSize-1; ix++) {
    for (int iy = 1; iy < field->ySize-1; iy++) {
      getNneighbours(field, ix, iy , &nNeighbours);
      field->fieldMatrixNeighbourCount[ix][iy] = nNeighbours;
    }
  }

  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      nNeighbours = field->fieldMatrixNeighbourCount[ix][iy];
      if (nNeighbours == 3) {
        field->fieldMatrix[ix][iy] = 1;
      } else if (nNeighbours < 2) {
        field->fieldMatrix[ix][iy] = 0;
      } else if (nNeighbours > 3) {
        field->fieldMatrix[ix][iy] = 0;
      }
    }
  }
}
