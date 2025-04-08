# import numpy as np
# import generate_inputs
# import matplotlib
#
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
#
# def load_in_streams():
#     with open('delayed_input.txt', 'r') as f:
#         dStream = int(''.join(line.strip() for line in f), 2)  # convert to binary
#
#     with open('regular_input.txt', 'r') as f:
#         rStream = int(''.join(line.strip() for line in f), 2)
#
#     return dStream, rStream
#
#
# def load_stream(filename):
#     with open(filename, 'r') as f:
#         return int(''.join(line.strip() for line in f), 2)
#
#
# if __name__ == '__main__':
#     generate_inputs
#     # Load both streams as integers with fixed length
#     dStream = load_stream('delayed_input.txt')
#     rStream = load_stream('regular_input.txt')
#
#
#
#     @profile
#     def findCoinciding(delayedStream, regularStream):
#         bestCoincidingCount = 0
#         bestDelay = 950
#         # recordedCoinciding = []
#         for i in range(950, 1051):
#             tempRegularStream = regularStream >> i
#
#             coincidingNum = delayedStream & tempRegularStream # and the two streams
#             coincidingCount = coincidingNum.bit_count()  # count the number of coinciding 1s
#             # recordedCoinciding.append(coincidingCount)
#
#             if bestCoincidingCount < coincidingCount:  # update bestDelay and bestCoincidingCount if necessary
#                 bestCoincidingCount = coincidingCount
#                 bestDelay = i
#
#         # plt.figure(figsize=(12, 6))
#         # plt.plot(recordedCoinciding, label="CoincidingVals")
#         # plt.xlabel("Offset from 950")
#         # plt.ylabel("Num Coinciding")
#         # plt.title("Num Coinciding Over the Offset from 950 to 1050")
#         # plt.legend()
#         # plt.show()
#
#         surroundingArr = np.zeros(10, int)  # look at surrounding values (+-5)
#         decreaseBy1 = False
#         for offset in range(-5, 6):
#             if offset == 0:  # if it isn't surrounding (just og val) don't include it
#                 decreaseBy1 = True
#                 continue
#
#             currDelay = offset + bestDelay
#             tempRegularStream = regularStream >> currDelay
#             coincidingNum = delayedStream & tempRegularStream
#             coincidingCount = coincidingNum.bit_count()
#
#             if decreaseBy1:
#                 offset -= 1
#             surroundingArr[5 + offset] = coincidingCount
#         return bestDelay, bestCoincidingCount, surroundingArr
#
#
#     optimalDelay, optimalCoinciding, surrounding = findCoinciding(dStream, rStream)
#     print(optimalDelay)
#     print(optimalCoinciding)
#     print(surrounding)
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Load the streams as NumPy arrays.
# ----------------------------
def load_stream(filename):
    # Assumes each line contains a single digit (0 or 1); loadtxt reads them as int.
    return np.loadtxt(filename, dtype=int)


# ----------------------------
# Shifting helper function.
# For a right shift (which "cuts off" the last d elements and pads d zeros at the start).
# ----------------------------
@profile
def shift_right(arr, d):
    if d <= 0:
        # For completeness, if d <= 0 we could instead shift left.
        return np.concatenate((arr[-d:], np.zeros(-d, dtype=arr.dtype)))
    # d > 0: shift right — pad with d zeros at beginning, remove d elements at the end.
    return np.concatenate((np.zeros(d, dtype=arr.dtype), arr[:-d]))


# ----------------------------
# Main execution
# ----------------------------
if __name__ == '__main__':
    # Load streams from file as vectorized NumPy arrays.
    delayed_stream = load_stream('delayed_input.txt')
    regular_stream = load_stream('regular_input.txt')

    # Verify the stream lengths:
    chunk_size = delayed_stream.size  # should be 100,000
    print("Stream length:", chunk_size)

    # Define candidate delay values (in samples) to test.
    delay_min = 950
    delay_max = 1050

    best_coinciding_count = -1
    best_delay = None
    # coincidence_counts = []  # record count per candidate delay

    # Loop over candidate delays:
    for d in range(delay_min, delay_max + 1):
        # Vectorized shift: shift the regular stream by 'd' samples to the right.
        shifted_regular = shift_right(regular_stream, d)
        # Compute element-wise AND (both arrays contain 0s and 1s, so this returns 1 when both are 1).
        coinciding = np.bitwise_and(delayed_stream, shifted_regular)
        # Sum the ones (vectorized)
        count = int(np.sum(coinciding))
        coincidence_counts.append(count)
        if count > best_coinciding_count:
            best_coinciding_count = count
            best_delay = d

    print("Optimal delay (samples):", best_delay)
    print("Optimal coinciding count:", best_coinciding_count)

    # Compute surrounding counts (from best_delay - 5 to best_delay + 5).
    surrounding_arr = np.zeros(11, dtype=int)  # 11 values for offsets -5 ... +5
    for offset in range(-5, 6):
        current_delay = best_delay + offset
        shifted_regular = shift_right(regular_stream, current_delay)
        coinciding = np.bitwise_and(delayed_stream, shifted_regular)
        surrounding_arr[offset + 5] = int(np.sum(coinciding))

    print("Surrounding counts (offsets -5 to +5):")
    print(surrounding_arr)

    # Plot the candidate delays vs. their coinciding counts.
    # delays = np.arange(delay_min, delay_max + 1)
    # plt.figure(figsize=(10, 5))
    # plt.plot(delays, coincidence_counts, 'o-', label="Coinciding count")
    # plt.xlabel("Delay (samples)")
    # plt.ylabel("Coinciding 1's count")
    # plt.title("Coinciding count vs. Delay")
    # plt.legend()
    # plt.show()

