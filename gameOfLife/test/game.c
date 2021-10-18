#include <stdio.h>
#include <stdlib.h>

#include "../src/gameOfLife.h"

int main() {
  matchField *game = malloc(sizeof(matchField));
  game->xSize = 10;
  game->ySize = 10;

  initMatchField(game);

  // game->fieldMatrix[5][5] = 1;
  // printMatchField(game);

  // applyIteration(game);

  // printMatchField(game);

  // freeMatchField(game);
  printf("end game \n");
}
