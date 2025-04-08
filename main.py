import numpy as np
import generate_inputs


def load_in_streams():
    with open('delayed_input.txt', 'r') as f:
        dStream = int(''.join(line.strip() for line in f), 2)  # convert to binary

    with open('regular_input.txt', 'r') as f:
        rStream = int(''.join(line.strip() for line in f), 2)

    return dStream, rStream


def load_stream(filename):
    with open(filename, 'r') as f:
        return int(''.join(line.strip() for line in f), 2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generate_inputs
    # Load both streams as integers with fixed length
    delayedStream = load_stream('delayed_input.txt')
    regularStream = load_stream('regular_input.txt')

    bestCoincidingCount = 0
    bestDelay = 950

    for i in range(950, 1051):
        tempRegularStream = regularStream >> i

        coincidingNum = delayedStream & tempRegularStream # and the two streams
        coincidingCount = coincidingNum.bit_count()  # count the number of coinciding 1s

        if bestCoincidingCount < coincidingCount:  # update bestDelay and bestCoincidingCount if necessary
            bestCoincidingCount = coincidingCount
            bestDelay = i

    surroundingArr = np.zeros(10, int)  # look at surrounding values (+-5)
    decreaseBy1 = False
    for offset in range(-5, 5):
        if offset == 0:  # if it isn't surrounding (just og val) don't include it
            decreaseBy1 = True
            continue

        currDelay = offset + bestDelay
        tempRegularStream = regularStream >> currDelay
        coincidingNum = delayedStream & tempRegularStream
        coincidingCount = bin(coincidingNum).count('1')

        if decreaseBy1:
            offset -= 1
        surroundingArr[5 + offset] = coincidingCount

    print(bestDelay)
    print(bestCoincidingCount)
    print(surroundingArr)
