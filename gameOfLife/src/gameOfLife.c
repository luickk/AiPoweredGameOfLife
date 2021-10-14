#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "gameOfLife.h"

struct matchField {
  int xSize, ySize;

  // using int for the sake of simplicity TODO: change to bitmask (don't know whether it's even worth the extra computing time)
  uint8_t **fieldMatrix;
};

struct twoDimCords {
  int x, y;
};

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
      switch (i) {
        case 0:
          if (cords->x > 0 && cords->x < gameField->xSize) {
            if (gameField->fieldMatrix[cords->x-1][cords->y] == 1) {
              nNeighbours++;
            }
          }
        case 1:
          if (cords->x > 0 && cords->x < gameField->xSize || cords->y > 0 && cords->y < gameField->ySize) {
            if (gameField->fieldMatrix[cords->x-1][cords->y+1] == 1) {
              nNeighbours++;
            }
          }
        case 2:
          if (cords->y > 0 && cords->y < gameField->ySize) {
            if (gameField->fieldMatrix[cords->x][cords->y+1] == 1) {
              nNeighbours++;
            }
          }
        case 3:
          if (cords->x > 0 && cords->x < gameField->xSize || cords->y > 0 && cords->y < gameField->ySize) {
            if (gameField->fieldMatrix[cords->x+1][cords->y+1] == 1) {
              nNeighbours++;
            }
          }
        case 4:
          if (cords->x > 0 && cords->x < gameField->xSize) {
            if (gameField->fieldMatrix[cords->x+1][cords->y] == 1) {
              nNeighbours++;
            }
          }
        case 5:
          if (cords->x > 0 && cords->x < gameField->xSize || cords->y > 0 && cords->y < gameField->ySize) {
            if (gameField->fieldMatrix[cords->x+1][cords->y-1] == 1) {
              nNeighbours++;
            }
          }
        case 6:
          if (cords->y > 0 && cords->y < gameField->ySize) {
            if (gameField->fieldMatrix[cords->x][cords->y-1] == 1) {
              nNeighbours++;
            }
          }
        case 7:
          if (cords->x > 0 && cords->x < gameField->xSize || cords->y > 0 && cords->y < gameField->ySize) {
            if (gameField->fieldMatrix[cords->x-1][cords->y-1] == 1) {
              nNeighbours++;
            }
          }
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
