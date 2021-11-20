import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Cython import gameOfLife



if __name__ == '__main__':
    x = np.load("latestRes.npy", allow_pickle=True)
    loss = x[0]
    reward = x[1]
    golMatchFieldDims = x[2]
    iterations = x[3]
    matchFieldMatrix = x[4]

    field = gameOfLife.matchFieldPy(golMatchFieldDims[0], golMatchFieldDims[1])
    field.zeroMatchFieldPy()
    field.fieldMatrix = matchFieldMatrix[0]

    print("============================================")
    print("Starting Match Field: ")
    print(field.fieldMatrix)
    print("Iterations: " + str(iterations))
    print("Match fiel Dims: " + str(golMatchFieldDims))
    print("============================================")

    plt.plot(loss, label="loss")
    plt.plot(reward, label="reward")
    plt.legend(loc="upper left")

    paused = False

    fig, ax = plt.subplots()
    matrice = ax.matshow(field.fieldMatrix)
    plt.colorbar(matrice)
    def update(i):
        field.applyIterationPy()
        matrice.set_array(field.fieldMatrix)
        # if i >= iterations:
        #     ani.event_source.stop()
    ani = animation.FuncAnimation(fig, update, repeat=True)
    plt.show()

    def togglePause(*args, **kwargs):
        print("toggled")
        if paused:
            ani.resume()
        else:
            ani.pause()
        paused = not paused

    fig.canvas.mpl_connect('button_press_event', togglePause)

    del field
