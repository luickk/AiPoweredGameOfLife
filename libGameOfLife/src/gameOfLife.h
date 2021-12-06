#include <stdint.h>

struct matchField{
  int xSize, ySize;

  int simpleComplexity;
  double entropy;
  double pComplexity;

  uint8_t *fieldMatrixNeighbourCount;

  // using int for the sake of simplicity TODO: change to bitmask (don't know whether it's even worth the extra computing time)
  uint8_t *fieldMatrix;
};

// internal
void getNneighbours(struct matchField *field, int x, int y, int *nNeighbours);

int fieldBoundaryCheck(struct matchField *field, int x, int y);

double calcLogWithBase(int base, double x);

int countCellsAlive(struct matchField *field);

int nLevensteinEncoding(int n);

// by https://www.geeksforgeeks.org/binomial-coefficient-dp-9/
int binomialCoeff(int n, int k);

// lib
void printMatchField(struct matchField *field);

void resetGame(struct matchField *field);

void setMatchFieldXY(struct matchField *field, int x, int y, int val);

void zeroMatchField(struct matchField *field);

void initMatchField(struct matchField *field);

void freeMatchField(struct matchField *field);

void applyIteration(struct matchField *field);

// !needs to be called per gol evolution!
void calcEntropy(struct matchField *field, int iteration);
void calcProbabilisticComplexity(struct matchField *field);
