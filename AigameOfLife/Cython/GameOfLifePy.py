import gameOfLife
import numpy as np

if __name__ == '__main__':
    field = gameOfLife.matchFieldPy(10, 10)
    field.zeroMatchFieldPy()

    field.fieldMatrix = np.ones((10,10), dtype=np.uint8)

    # field.printMatchFieldPy()
    # print(field.fieldMatrix)

    field.zeroMatchFieldPy()

    field.setMatchFieldXYpy(5, 5, 1);
    field.setMatchFieldXYpy(6, 5, 1);
    field.setMatchFieldXYpy(7, 5, 1);

    for i in range(10):
        field.applyIterationPy()
        field.calcEntropyPy(i)
        print("simple Complexity: " + str(field.simpleComplexity))
        print("entropy: %.6f"%field.entropy)
        print(field.fieldMatrix)

    del field
