import gameOfLife

if __name__ == '__main__':
    field = gameOfLife.matchFieldPy(10, 10)
    field.zeroMatchFieldPy()
    field.printMatchFieldPy()

    print(field.fieldMatrix)

    del field
