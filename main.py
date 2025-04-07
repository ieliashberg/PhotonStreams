# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# NAIVE IMPLEMENTATION
# take the delayed array and subtract from it 950 to 1050
# figure out where there is the most correlation, and what the value of the correlation is
# have an array of size 1000 that holds the current samples (and potentially
#    one computed ahead array so you aren't behind by more than 1000 samples (or whatever the step size is)
# Assuming you now have 2 arrays, compute correlation function

def load_in_streams():
    with open('delayed_input.txt', 'r') as f:
        dStream = int(''.join(line.strip() for line in f))

    with open('regular_input.txt', 'r') as f:
        rStream = int(''.join(line.strip() for line in f))

    return dStream, rStream


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    delayedStream, regularStream = load_in_streams()
    for i in range(950, 1051):
        tempDelayedStream = delayedStream % (10 ** (100000 - i))     # get the shifted delayedStream by cutting of the first i
        tempRegularStream = delayedStream // (10 ** i)    # get the shifted regularStream by cutting off the last i

