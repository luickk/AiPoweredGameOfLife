import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep

from Cython import gameOfLife



if __name__ == '__main__':
    x = np.load("latestRes.npy", allow_pickle=True)
    graphicSaved = False

    loss = x[0]
    reward = x[1]
    golMatchFieldDims = x[2]
    iterations = x[3]
    matchFieldMatrix = x[4]
    trainingStats = x[5]

    num_iterations = trainingStats[0]
    actor_learning_rate = trainingStats[1]
    critic_learning_rate = trainingStats[2]
    batch_size = trainingStats[3]
    fc_layer_params = trainingStats[4]
    observation_fc_layer_params = trainingStats[5]

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

    fig, ax = plt.subplots(figsize=(5, 8))
    matrice = ax.matshow(field.fieldMatrix)
    framesAnnotation = plt.annotate('Frames', (0,0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('nn it:' +str(num_iterations), (0,0), (0, -30), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('gol it:' + str(iterations), (0,0), (0, -40), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('batchS:' + str(batch_size), (0,0), (0, -50), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('fc_layer_params:' + str(fc_layer_params), (0,0), (0, -60), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('observation_fc_layer_params:' + str(observation_fc_layer_params), (0,0), (0, -70), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('actor lr:' + str(actor_learning_rate), (0,0), (0, -80), xycoords='axes fraction', textcoords='offset points', va='top')
    plt.annotate('critic lr:' + str(critic_learning_rate), (0,0), (0, -90), xycoords='axes fraction', textcoords='offset points', va='top')

    def update(i):
        global graphicSaved
        if i <= iterations:
            field.applyIterationPy()
            matrice.set_array(field.fieldMatrix)
            framesAnnotation.set_text(str(i))
            if i == iterations and not graphicSaved:
                graphicSaved = True
                ani.event_source.stop()
                sleep(1)
                ani.save('../resultsAnitmations/'+str(random.randint(0, 100))+'.gif', writer='imagemagick')
                print("gif saved")

    ani = animation.FuncAnimation(fig, update)
    plt.show()

    del field
