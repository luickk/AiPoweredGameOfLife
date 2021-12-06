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

  printf("init matrix: \n");
  printMatchField(game);
  printf("------------ \n");

  for(int i = 1; i <= nIteration; i++) {
    applyIteration(game);
    calcEntropy(game, i);
    calcProbabilisticComplexity(game);

    printMatchField(game);
    printf("iteration %d: \n", i);
    printf("entropy: %f \n", game->entropy);
    printf("simple complexity: %d \n", game->simpleComplexity);
    printf("probabilistic complexity: %f \n", game->pComplexity);
  }
  freeMatchField(game);

  printf("end game \n");
}
