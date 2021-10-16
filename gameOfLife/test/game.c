#include <stdio.h>
#include <stdlib.h>

#include "../src/gameOfLife.h"

int main() {
  matchField *game = malloc(sizeof(matchField));
  game->xSize = 100;
  game->ySize = 100;

  initMatchField(game);

  applyIteration(game);

  printf("end game \n");

  freeMatchField(game);
}
