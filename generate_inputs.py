import numpy as np
import random

# params
maxDelayValChange = 10  # represents the max delay change from 1 photon to the next
noise0to1 = 0.01  # chance 0 becoming 1
noise1to0 = 0.1  # chance 1 becoming 0
maxShift = 2  # how far a 1 can shift when adding noise
shiftProb = 0.1  # probability that a 1 shifts when adding noise

prevDelayVal = random.randint(950, 1050)  # declare and initialize the prevDelayVal
regularArr = np.random.choice([0, 1], size=100000, p=[0.8, 0.2])  # declaring and initializing delayedArr
delayedArr = np.zeros(100000, int)  # initializing everything in delay channel to 0
for i in range(100000):  # loop over everything in the d and for each 1 generate a delay
    if regularArr[i] == 1:
        delayChange = random.randint(-maxDelayValChange, maxDelayValChange)
        if (i + delayChange + prevDelayVal) < 100000:       # if the new index is in bounds, make it 1
            delayedArr[i + delayChange + prevDelayVal] = 1
            prevDelayVal = delayChange + prevDelayVal       # update the prevDelayVal


def add_noise(arr):
    noisyArr = arr.copy()
    for j in range(100000):
        if arr[j] == 1:  # if sample is 1
            if random.random() < noise1to0:  # see if you need to change from 1 to 0
                noisyArr[j] = 0
            elif random.random() < shiftProb:  # check if you need to shift the 1 +-2 (max)
                shift = int(np.random.triangular(-maxShift, 0, maxShift))  # generate the shift amount
                noisyArr[j] = 0  # remove the sample from current location
                if 0 <= j + shift < 100000:     # check bounds for shift and shift if in bounds
                    noisyArr[j + shift] = 1
        else:
            if random.random() < noise0to1:     # if 0, check to see if should switch to 1
                noisyArr[j] = 1
    return noisyArr


delayedArr = add_noise(delayedArr)

with open('regular_input.txt', 'w') as f:  # write to the regular_input.txt file
    for val in regularArr:
        f.write(str(val) + "\n")

with open('delayed_input.txt', 'w') as f:  # write to the delayed_input.txt file
    for val in delayedArr:
        f.write(str(val) + "\n")
