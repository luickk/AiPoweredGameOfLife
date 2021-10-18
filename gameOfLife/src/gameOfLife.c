#include <stdio.h>
#include <stdlib.h>

#include "gameOfLife.h"

void zeroMatchField(matchField *field) {
  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      field->fieldMatrix[ix][iy] = 0;
    }
  }
}

void printMatchField(matchField *field) {
  for (int ix = 0; ix < field->xSize; ix++) {
    for (int iy = 0; iy < field->ySize; iy++) {
      printf("%d", field->fieldMatrix[ix][iy]);
    }
    printf("\n");
  }
}

void initMatchField(matchField *field) {
  field->fieldMatrix = malloc(field->xSize * sizeof(int*));
  for (int i = 0; i < field->ySize; i++) {
    field->fieldMatrix[i] = malloc(field->ySize * sizeof(int));
  }
  zeroMatchField(field);
}

void freeMatchField(matchField *field) {
  free(field->fieldMatrix);
  free(field);
}

int fieldBoundaryCheck(matchField *field, fieldCords *cords) {
  if (field->xSize >= cords->x && field->ySize >= cords->y) {
    return 1;
  }
  return 0;
}

void getNneighbours(matchField *field, fieldCords *cords, int *nNeighbours) {
  nNeighbours = 0;
  if (fieldBoundaryCheck(field, cords)) {
    if (cords->x > 0 && cords->x < field->xSize) {
      nNeighbours += field->fieldMatrix[cords->x-1][cords->y];
      nNeighbours += field->fieldMatrix[cords->x+1][cords->y];
    } else if (cords->x > 0 && cords->x < field->xSize || cords->y > 0 && cords->y < field->ySize) {
      nNeighbours += field->fieldMatrix[cords->x-1][cords->y+1];
      nNeighbours += field->fieldMatrix[cords->x+1][cords->y+1];
      nNeighbours += field->fieldMatrix[cords->x+1][cords->y-1];
      nNeighbours += field->fieldMatrix[cords->x-1][cords->y-1];
    } else if (cords->y > 0 && cords->y < field->ySize) {
      nNeighbours += field->fieldMatrix[cords->x][cords->y+1];
      nNeighbours += field->fieldMatrix[cords->x][cords->y-1];
    }
  }
}

void applyIteration(matchField *field) {
  int nNeighbours = 0;
  fieldCords cords = {0, 0};

  for (int ix; ix < field->xSize; ix++) {
    for (int iy; iy < field->ySize; iy++) {
      cords.x = ix;
      cords.y = iy;
      getNneighbours(field, &cords, &nNeighbours);

      if (nNeighbours < 1) {
        field->fieldMatrix[ix][iy] = 0;
      } else if (nNeighbours == 2) {
        field->fieldMatrix[ix][iy] = 1;
      } else if (nNeighbours > 2) {
        field->fieldMatrix[ix][iy] = 0;
      }
    }
  }
}
