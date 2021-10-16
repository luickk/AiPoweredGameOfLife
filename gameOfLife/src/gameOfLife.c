#include <stdio.h>
#include <stdlib.h>

#include "gameOfLife.h"


void initMatchField(matchField *gameField) {
  gameField->fieldMatrix = malloc(sizeof(uint8_t) * gameField->xSize * gameField->ySize);
}

void freeMatchField(matchField *gameField) {
  free(gameField->fieldMatrix);
  free(gameField);
}

int fieldBoundaryCheck(matchField *gameField, fieldCords *cords) {
  if (gameField->xSize >= cords->x && gameField->ySize >= cords->y) {
    return 1;
  }
  return 0;
}

void getNneighbours(matchField *gameField, fieldCords *cords, int *nNeighbours) {
  nNeighbours = 0;
  if (fieldBoundaryCheck(gameField, cords)) {
    for (int i; i <= 7; i++) {
      if (cords->x > 0 && cords->x < gameField->xSize) {
        nNeighbours += gameField->fieldMatrix[cords->x-1][cords->y];
        nNeighbours += gameField->fieldMatrix[cords->x+1][cords->y];
      } else if (cords->x > 0 && cords->x < gameField->xSize || cords->y > 0 && cords->y < gameField->ySize) {
        nNeighbours += gameField->fieldMatrix[cords->x-1][cords->y+1];
        nNeighbours += gameField->fieldMatrix[cords->x+1][cords->y+1];
        nNeighbours += gameField->fieldMatrix[cords->x+1][cords->y-1];
        nNeighbours += gameField->fieldMatrix[cords->x-1][cords->y-1];
      } else if (cords->y > 0 && cords->y < gameField->ySize) {
        nNeighbours += gameField->fieldMatrix[cords->x][cords->y+1];
        nNeighbours += gameField->fieldMatrix[cords->x][cords->y-1];
      }
    }
  }
}

void applyIteration(matchField *gameField) {
  int nNeighbours = 0;
  fieldCords cords = {0, 0};

  for (int ix; ix <= gameField->xSize; ix++) {
    for (int iy; iy <= gameField->ySize; iy++) {
      cords.x = ix;
      cords.y = iy;
      getNneighbours(gameField, &cords, &nNeighbours);

      if (nNeighbours < 1) {
        gameField->fieldMatrix[ix][iy] = 0;
      } else if (nNeighbours == 2) {
        gameField->fieldMatrix[ix][iy] = 1;
      } else if (nNeighbours > 2) {
        gameField->fieldMatrix[ix][iy] = 0;
      }
    }
  }
}
