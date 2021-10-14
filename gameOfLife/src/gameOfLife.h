
typedef struct matchField matchField;
typedef struct twoDimCords fieldCords;

void initMatchField(matchField *gameField);

void freeMatchField(matchField *gameField);

int fieldBoundaryCheck(matchField *gameField, fieldCords *cords);

void getNneighbours(matchField *gameField, fieldCords *cords, int *nNeighbours);

void applyIteration(matchField *gameField);
