#include <stdio.h>
#include <stdlib.h>

#include "../src/gameOfLife.h"

int main() {
  matchField *game = malloc(sizeof(matchField));
  game->xSize = 10;
  game->ySize = 10;

  initMatchField(game);

  applyIteration(game);

  printf("end game \n");

  printMatchField(game);

  freeMatchField(game);
}
