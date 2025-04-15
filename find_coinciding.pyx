# We are using pure C types for loop variables and counters.
# @profile
def findCoinciding(object delayedStream, object regularStream):
    cdef int bestCoincidingCount = 0
    cdef int bestDelay = 950
    cdef int i, offset, currDelay, coincidingCount

    # Loop over candidate delays from 950 to 1050 (inclusive).
    for i in range(950, 1051):
        # Python ints remain as objects;
        # we rely on the underlying C implementation for bit-shift and bit_count.
        tempRegularStream = regularStream >> i
        coincidingNum = delayedStream & tempRegularStream
        # Call the Python bit_count method (this is a C-level call in CPython 3.10+, but if you're on 3.9, you'll get the equivalent using bin() if needed)
        coincidingCount = coincidingNum.bit_count()
        if bestCoincidingCount < coincidingCount:
            bestCoincidingCount = coincidingCount
            bestDelay = i

    # Build surrounding counts in an array of length 11 (from offset -5 to +5)
    surroundingArr = [0] * 11
    for offset in range(-5, 6):
        currDelay = bestDelay + offset
        tempRegularStream = regularStream >> currDelay
        coincidingNum = delayedStream & tempRegularStream
        coincidingCount = coincidingNum.bit_count()
        surroundingArr[offset + 5] = coincidingCount

    return bestDelay, bestCoincidingCount, surroundingArr