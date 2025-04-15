import numpy as np
import random
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# params
noise0to1 = 0.01  # chance 0 becoming 1
noise1to0 = 0.1  # chance 1 becoming 0
maxJitter = 2  # how far a 1 can shift when adding noise
shiftProb = 0.1  # probability that a 1 shifts when adding noise
bigJumpProb = 0.000000001  # probability of a big jump occurring (around 30)
bigJumpSize = 30  # size of a big jump
chunkSize = 100000
maxDelayVariation = 50  # where the delay can wander
expectedDelay = 1000

regularArr = np.random.choice([0, 1], size=chunkSize, p=[0.8, 0.2])  # declaring and initializing regularArr


def generate_delayed_stream():
    delay_history = []
    delayedStream = np.zeros(chunkSize, int)  # initializing everything in delay channel to 0
    currentDelay = float(random.random() * 100 + (expectedDelay - maxDelayVariation))  # generate an initial delay

    for i in range(chunkSize):  # loop over everything in the d and for each 1 generate a delay
        # random walk - update current delay with small step
        step = random.uniform(-0.1, 0.1)
        currentDelay += step
        if regularArr[i] == 1:
            updateDelay = currentDelay
            # occasionally, add an infrequent big jump
            if random.random() < bigJumpProb:
                bigJump = random.uniform(-bigJumpSize, bigJumpSize)
                updateDelay += bigJump

            # add fixed jitter
            jitter = 0
            if random.random() < shiftProb:
                jitter = random.uniform(-maxJitter, maxJitter)

            roundedFinalDelay = int(round(updateDelay + jitter))
            roundedFinalDelay = max(expectedDelay - maxDelayVariation,
                                    roundedFinalDelay)  # make sure delay is in bounds of the max delay
            roundedFinalDelay = min(expectedDelay + maxDelayVariation, roundedFinalDelay)

            delay_index = i + roundedFinalDelay
            delay_history.append(roundedFinalDelay)

            # print(roundedFinalDelay)
            # only updated delay stream if in bounds
            if 0 <= delay_index < chunkSize:
                delayedStream[delay_index] = 1

    for j in range(chunkSize):
        if delayedStream[j] == 1:  # if sample is 1
            if random.random() < noise1to0:  # see if you need to change from 1 to 0
                delayedStream[j] = 0
        else:
            if random.random() < noise0to1:  # if 0, check to see if should switch to 1
                delayedStream[j] = 1
    return delayedStream, delay_history


def generateInputs():
    delayedArr, delayHistory = generate_delayed_stream()

    # for visualizing the actual generated delay

    # plt.figure(figsize=(12, 6))
    # plt.plot(delayHistory, label="Delayed")
    # plt.xlabel("Sample Index")
    # plt.ylabel("Delay Value")
    # plt.title("Delay Evolution Over Samples")
    # plt.legend()
    # plt.show()

    with open('regular_input.txt', 'w') as f:  # write to the regular_input.txt file
        for val in regularArr:
            f.write(str(val) + "\n")

    with open('delayed_input.txt', 'w') as f:  # write to the delayed_input.txt file
        for val in delayedArr:
            f.write(str(val) + "\n")
