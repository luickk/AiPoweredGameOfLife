#include <stdio.h>
#include <stdlib.h>

#include "../src/gameOfLife.h"

int main() {
  struct matchField *game = malloc(sizeof(struct matchField));
  game->xSize = 10;
  game->ySize = 10;

  int nIteration = 10;

  initMatchField(game);

  setMatchFieldXY(game, 5, 5, 1);
  setMatchFieldXY(game, 6, 5, 1);
  setMatchFieldXY(game, 7, 5, 1);

  printf("pre iteration: \n");
  printMatchField(game);

  for(int i = 0; i <= nIteration; i++) {
    applyIteration(game);
    printf("iteration %d: \n", i);
    printMatchField(game);
  }

  freeMatchField(game);

  printf("end game \n");
}
