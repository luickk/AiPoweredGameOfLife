#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "gameOfLife.h"

// direct memory layout indexing
#define D_MEM_INDEX(X, Y, Y_SIZE)  (X+Y_SIZE*Y)

void zeroMatchField(struct matchField *field) {
  for (int i = field->twoDsize; i--;) {
      field->fieldMatrix[i] = 0;
  }
}

void setMatchFieldXY(struct matchField *field, int x, int y, int val) {
  field->fieldMatrix[D_MEM_INDEX(x, y, field->ySize)] = val;
}

void printMatchField(struct matchField *field) {
  for (int ix = field->xSize; ix--;) {
    for (int iy = field->ySize; iy--;) {
      printf("%d", field->fieldMatrix[D_MEM_INDEX(ix, iy, field->ySize)]);
    }
    printf("\n");
  }
}

void initMatchField(struct matchField *field) {
  field->twoDsize = field->xSize * field->ySize;
  // direct memory layout in order to be compatible with python memory protocols
  field->fieldMatrixNeighbourCount = malloc(field->twoDsize * sizeof(uint8_t*));
  field->fieldMatrix = malloc(field->twoDsize * sizeof(uint8_t*));

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
  field->pComplexity = 0;
}

double calcLogWithBase(int base, double x) {
  return log(x)/log(base);
}

double nLevensteinEncoding(int n) {
  return (log2(n+1)+log2(n))+1;
}

// due its unsorted nature I decided not to implement a partition of quick scan count
int countCellsAlive(struct matchField *field) {
  int cellsAlive=0;
  for (int i = field->twoDsize; i--;) {
    if (field->fieldMatrix[i]) {
      cellsAlive++;
    }
  }
  return cellsAlive;
}

// by https://www.geeksforgeeks.org/binomial-coefficient-dp-9/
int binomialCoeff(int n, int k)
{
    // Base Cases
    if (k > n)
        return 0;
    if (k == 0 || k == n)
        return 1;

    // Recur
    return binomialCoeff(n - 1, k - 1)
           + binomialCoeff(n - 1, k);
}

// by https://www.geeksforgeeks.org/binomial-coefficient-dp-9/
int min(int a, int b) { return (a < b) ? a : b; }

// by https://www.geeksforgeeks.org/binomial-coefficient-dp-9/
int fastBinomialCoeff(int n, int k)
{
    int C[n + 1][k + 1];
    int i, j;

    // Calculate value of Binomial Coefficient
    // in bottom up manner
    for (i = 0; i <= n; i++) {
      for (j = 0; j <= min(i, k); j++) {
            // Base Cases
            if (j == 0 || j == i)
                C[i][j] = 1;

            // Calculate value using
            // previously stored values
            else
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j];
        }
    }

    return C[n][k];
}

void calcProbabilisticComplexity(struct matchField *field) {
  field->cellsAlive = countCellsAlive(field);
  field->pComplexity = nLevensteinEncoding(field->xSize) + nLevensteinEncoding(field->ySize) + nLevensteinEncoding(field->cellsAlive) + log2(fastBinomialCoeff(field->twoDsize, field->cellsAlive));
}

// !needs to be called per iteration!
void calcEntropy(struct matchField *field, int iteration) {
  field->entropy = ((double)1/(double)(field->twoDsize)) * calcLogWithBase(iteration, (double)(field->twoDsize)/(double)countCellsAlive(field));
}

int fieldBoundaryCheck(struct matchField *field, int x, int y) {
  if (field->xSize >= x && field->ySize >= y) {
    return 1;
  }
  return 0;
}

void getCellNeighbours(struct matchField *field, int *x, int *y, uint8_t *nNeighbours) {
  *nNeighbours = 0;
  *nNeighbours += field->fieldMatrix[D_MEM_INDEX((*x-1), *y, field->ySize)] + field->fieldMatrix[D_MEM_INDEX((*x+1), *y, field->ySize)]
                + field->fieldMatrix[D_MEM_INDEX((*x-1), (*y+1), field->ySize)] + field->fieldMatrix[D_MEM_INDEX((*x+1), (*y+1), field->ySize)]
                + field->fieldMatrix[D_MEM_INDEX((*x+1), (*y-1), field->ySize)] + field->fieldMatrix[D_MEM_INDEX((*x-1), (*y-1), field->ySize)]
                + field->fieldMatrix[D_MEM_INDEX(*x, (*y+1), field->ySize)] + field->fieldMatrix[D_MEM_INDEX(*x, (*y-1), field->ySize)];
}
void applyIteration(struct matchField *field) {
  field->simpleComplexity = 0;
  for (int ix = 1; ix < field->xSize-1; ix++) {
    for (int iy = 1; iy < field->ySize-1; iy++) {
      getCellNeighbours(field, &ix, &iy, &field->fieldMatrixNeighbourCount[D_MEM_INDEX(ix, iy, field->ySize)]);
    }
  }
  for (int i = field->twoDsize; i--;) {
   if (field->fieldMatrixNeighbourCount[i] == 3) {
     field->fieldMatrix[i] = 1;
     field->simpleComplexity += 1;
   } else if (field->fieldMatrixNeighbourCount[i] < 2) {
     field->fieldMatrix[i] = 0;
     field->simpleComplexity += 1;
   } else if (field->fieldMatrixNeighbourCount[i] > 3) {
     field->fieldMatrix[i] = 0;
     field->simpleComplexity += 1;
   }
 }
}
