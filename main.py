import numpy as np


def load_in_streams():
    with open('delayed_input.txt', 'r') as f:
        dStream = int(''.join(line.strip() for line in f), 2)  # convert to binary representation from the file

    with open('regular_input.txt', 'r') as f:
        rStream = int(''.join(line.strip() for line in f), 2)

    return dStream, rStream


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    delayedStream, regularStream = load_in_streams()
    bestCoincidingCount = 0
    bestDelay = 950

    for i in range(950, 1051):
        tempDelayedStream = delayedStream << i  # get the shifted delayedStream by cutting of the first i
        tempRegularStream = regularStream >> i  # get the shifted regularStream by cutting off the last i

        coincidingNum = tempDelayedStream & tempRegularStream  # and the two streams
        coincidingCount = bin(coincidingNum).count('1')  # count the number of coinciding 1s

        if bestCoincidingCount < coincidingCount:  # update bestDelay and bestCoincidingCount if necessary
            bestCoincidingCount = coincidingCount
            bestDelay = i

    surroundingArr = np.zeros(10, int)  # look at surrounding values (+-5)
    for offset in range(-5, 5):
        if offset == 0:  # if it isn't surrounding (just og val) don't include it
            continue
        currDelay = offset + bestDelay
        tempDelayedStream = delayedStream << currDelay
        tempRegularStream = regularStream >> currDelay
        coincidingNum = tempDelayedStream & tempRegularStream
        coincidingCount = bin(coincidingNum).count('1')

        surroundingArr[5 + offset] = coincidingCount  # add to surroundArr

    print(bestDelay)
    print(bestCoincidingCount)
    print(surroundingArr)
