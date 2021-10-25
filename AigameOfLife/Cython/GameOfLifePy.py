import gameOfLife

if __name__ == '__main__':
    field = gameOfLife.matchFieldPy(100, 100)
    field.zeroMatchFieldPy()
    del field
