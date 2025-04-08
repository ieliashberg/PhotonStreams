import numpy as np
import generate_inputs
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def load_in_streams():
    with open('delayed_input.txt', 'r') as f:
        dStream = int(''.join(line.strip() for line in f), 2)  # convert to binary

    with open('regular_input.txt', 'r') as f:
        rStream = int(''.join(line.strip() for line in f), 2)

    return dStream, rStream


def load_stream(filename):
    with open(filename, 'r') as f:
        return int(''.join(line.strip() for line in f), 2)


if __name__ == '__main__':
    generate_inputs
    # Load both streams as integers with fixed length
    dStream = load_stream('delayed_input.txt')
    rStream = load_stream('regular_input.txt')



    @profile
    def findCoinciding(delayedStream, regularStream):
        bestCoincidingCount = 0
        bestDelay = 950
        # recordedCoinciding = []
        for i in range(950, 1051):
            tempRegularStream = regularStream >> i

            coincidingNum = delayedStream & tempRegularStream # and the two streams
            coincidingCount = coincidingNum.bit_count()  # count the number of coinciding 1s
            # recordedCoinciding.append(coincidingCount)

            if bestCoincidingCount < coincidingCount:  # update bestDelay and bestCoincidingCount if necessary
                bestCoincidingCount = coincidingCount
                bestDelay = i

        # plt.figure(figsize=(12, 6))
        # plt.plot(recordedCoinciding, label="CoincidingVals")
        # plt.xlabel("Offset from 950")
        # plt.ylabel("Num Coinciding")
        # plt.title("Num Coinciding Over the Offset from 950 to 1050")
        # plt.legend()
        # plt.show()

        surroundingArr = np.zeros(10, int)  # look at surrounding values (+-5)
        decreaseBy1 = False
        for offset in range(-5, 6):
            if offset == 0:  # if it isn't surrounding (just og val) don't include it
                decreaseBy1 = True
                continue

            currDelay = offset + bestDelay
            tempRegularStream = regularStream >> currDelay
            coincidingNum = delayedStream & tempRegularStream
            coincidingCount = coincidingNum.bit_count()

            if decreaseBy1:
                offset -= 1
            surroundingArr[5 + offset] = coincidingCount
        return bestDelay, bestCoincidingCount, surroundingArr


    optimalDelay, optimalCoinciding, surrounding = findCoinciding(dStream, rStream)
    print(optimalDelay)
    print(optimalCoinciding)
    print(surrounding)
