import generate_inputs
import load_stream_module
import find_coinciding
# import matplotlib # for visualization if wanted
import time
import mmap


# also just for visualization purposes
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt


# Simple python implementation of loading the streams for comparison (not currently used)
def load_stream(inputFile):
    with open(inputFile, 'r') as f:
        # memory map the whole file (length = 0 means the whole file)
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        # read entire contents from memory map
        s = mm.read().decode('ascii')
        # close the map
        mm.close()
    # Remove any whitespace characters
    s = s.replace("\n", "").replace(" ", "")

    # return base 2 integer representation of the input
    return int(s, 2)


# calculates correlation, strict python function (not currently used)
def findCoinciding(delayedStream, regularStream):
    bestCoincidingCount = 0
    bestDelay = 950
    # recordedCoinciding = []       # for visualization
    for i in range(950, 1051):
        tempRegularStream = regularStream >> i
        coincidingNum = delayedStream & tempRegularStream  # and the two streams
        coincidingCount = coincidingNum.bit_count()  # count the number of coinciding 1s
        # recordedCoinciding.append(coincidingCount) # for visualization
        if bestCoincidingCount < coincidingCount:  # update bestDelay and bestCoincidingCount if necessary
            bestCoincidingCount = coincidingCount
            bestDelay = i

    # Visualization of correlation function
    # plt.figure(figsize=(12, 6))
    # plt.plot(recordedCoinciding, label="CoincidingVals")
    # plt.xlabel("Offset from 950")
    # plt.ylabel("Num Coinciding")
    # plt.title("Num Coinciding Over the Offset from 950 to 1050")
    # plt.legend()
    # plt.show()

    surroundingArr = [0] * 11
    for offset in range(-5, 6):
        currDelay = bestDelay + offset
        tempRegularStream = regularStream >> currDelay
        coincidingNum = delayedStream & tempRegularStream
        coincidingCount = coincidingNum.bit_count()
        surroundingArr[offset + 5] = coincidingCount

    return bestDelay, bestCoincidingCount, surroundingArr


def main():
    # debug stuff to seeing how fast the IO and the find_coinciding function is
    totalIOTime = 0
    totalFuncTime = 0

    iterations = 100
    for i in range(iterations):
        generate_inputs.generateInputs()

        startIO = time.time()  # start IO time - strictly for timing

        # Using c module for IO, load in the 2 photon streams
        dStream = load_stream_module.load_stream('delayed_input.txt')
        rStream = load_stream_module.load_stream('regular_input.txt')

        # pure python for loading 2 photon streams (only for comparison to c module speed)
        # dStream = load_stream('delayed_input.txt')
        # rStream = load_stream('regular_input.txt')

        endIO = time.time()  # ending the IO time
        totalIOTime += endIO - startIO  # add this IO time to total IO time

        startFunc = time.time()  # timing the find_coinciding function

        # strict python implementation of correlation function (only for comparison to cython speed)
        # optimalDelay, optimalCoinciding, surrounding = findCoinciding(dStream, rStream)

        # correlation function implementation using cython module
        optimalDelay, optimalCoinciding, surrounding = find_coinciding.findCoinciding(dStream, rStream)

        # can comment out this section if you don't want to see the output (slows down a lot if you print)
        # print(optimalDelay)
        # print(optimalCoinciding)
        # print(surrounding)

        endFunc = time.time()  # end time for find_Coinciding
        totalFuncTime += endFunc - startFunc  # add time to total find_coinciding time

    # also here just to check timing (can comment this section out)
    print("averageIOTime:", totalIOTime / iterations)
    print("averageFuncTime:", totalFuncTime / iterations)
    print("average total time:", (totalIOTime / iterations) + (totalFuncTime / iterations))
    print("total time:", totalIOTime + totalFuncTime)


# separate from actual main so it was easier to profile the correlation function (not necessary profiling not needed)
# We can move all our code to here if necessary
if __name__ == '__main__':
    main()


# End to end Implementation using multithreading (for some reason turned out to be slower than single threaded implementation)
# import threading
# import queue
# import time
# import generate_inputs
# import load_stream_module
# import find_coinciding
#
# # maxsize prevents producer from getting too far ahead of consumer
# data_queue = queue.Queue(maxsize=10)
#
# NUM_ITERATIONS = 1000
# totalTimeForConsumer = 0.0
# totalTimeForProducer = 0.0
#
#
# # thread that reads input files and puts them on the queue
# def producer():
#     global totalTimeForProducer
#     startProducer = time.time()
#     for _ in range(NUM_ITERATIONS):
#
#         generate_inputs.generateInputs()
#
#         # load streams using c module
#         dStream = load_stream_module.load_stream('delayed_input.txt')
#         rStream = load_stream_module.load_stream('regular_input.txt')
#
#         # put streams into queue
#         data_queue.put((dStream, rStream))
#     # signal completion to consumer
#     data_queue.put(None)
#     endProducer = time.time()
#     totalTimeForProducer = endProducer - startProducer
#
#
# # thread that processes data from the queue.
# def consumer():
#     global totalTimeForConsumer
#     startConsumer = time.time()
#     iteration = 0
#     while True:
#         item = data_queue.get()
#         if item is None:
#             data_queue.task_done()  # mark  sentinel as done
#             break
#         dStream, rStream = item
#
#         bestDelay, bestCoinciding, surrounding = find_coinciding.findCoinciding(dStream, rStream)
#
#         print(
#             f"Iteration {iteration}: Optimal delay: {bestDelay}, Coinciding: {bestCoinciding}, Surrounding: {surrounding}")
#         iteration += 1
#
#         data_queue.task_done()
#     endConsumer = time.time()
#     totalTimeForConsumer = endConsumer - startConsumer
#
#
# # create and start threads
# producer_thread = threading.Thread(target=producer, name="Producer", daemon=True)
# consumer_thread = threading.Thread(target=consumer, name="Consumer", daemon=True)
#
# start_time = time.time()
# producer_thread.start()
# consumer_thread.start()
#
# # wait till both threads finish
# producer_thread.join()
# consumer_thread.join()
# end_time = time.time()
#
# print("Total producer time:", totalTimeForProducer, "seconds")
# print("Total consumer time:", totalTimeForConsumer, "seconds")
# print("Total processing time:", end_time - start_time, "seconds")
