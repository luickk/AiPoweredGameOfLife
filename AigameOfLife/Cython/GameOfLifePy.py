import gameOfLife
import numpy as np

if __name__ == '__main__':
    field = gameOfLife.matchFieldPy(10, 10)
    field.zeroMatchFieldPy()

    field.printMatchFieldPy()
    print(field.fieldMatrix)

    field.fieldMatrix = np.ones((10,10), dtype=np.uint8)

    field.printMatchFieldPy()
    print(field.fieldMatrix)

    del field
