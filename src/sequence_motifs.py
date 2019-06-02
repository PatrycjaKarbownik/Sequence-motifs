import sys

from Network import Network
from input_patterns import load
import random

def printHelp():
    print("................................................................................................")
    print("Wrong arguments. Check if they meet reguirements:                                              |")
    print("- FILE_NAME           -> file with sequences, for example: \"data2.txt\"                         |")
    print("- SEQ_SIZE            -> motifs' length (minimum 4)                                            |")
    print("- LAYERS_AMOUNT       -> how many layers the network will have (minimum 2)                     |")
    print("- MAX_ERROR           -> max number of nucleotides differences in motif (minimum 0)            |")
    print("- TRESHHOLD_SEQ_AMOUNT-> minimum number of sequences which decide if it is a motif (minimum 2) |")
    print("- TRESHHOLD_VALUES    -> (LAYERS_AMOUNT - 1) float numbers between 0 and 1                     |")
    print("------------------------------------- EXAMPLE --------------------------------------------------")
    print("|                                                                                              |")
    print("|                python sequence_motifs.py \"data2.txt\" 5 3 5 4 0.2 0.4                         |")
    print("|                                                                                              |")
    print("------------------------------------------------------------------------------------------------")

def checkValues(argList, count):
    if not isinstance(argList[1], str) or (argList[1].count(".txt") != 1):
        return False
    if argList[2] < 4:
        return False
    if argList[3] < 2:
        return False
    if argList[4] < 0:
        return False
    if argList[5] < 2:
        return False
    iterator = 6
    while iterator < count:
        if argList[iterator] < 0 or argList[iterator] > 1:
            return False
        iterator = iterator+1
    return True

if __name__ == "__main__":
    argList = sys.argv
    if len(argList) < 4 or len(argList) != 5+int(argList[3]):
        print()
        printHelp()
    else:
        count = 5 + int(argList[3])
        i = 2
        while i < 6:
            argList[i] = int(argList[i])
            i = i+1
        while i < count:
            argList[i] = float(argList[i])
            i = i+1
        if not checkValues(argList, count):
            print("................................................................................................")
            print("Number of arguments good, but wrong values...                                                  |")
            printHelp()
        else:
            TreshholdValues = []
            i = 6
            while i < count:
                TreshholdValues.append(argList[i])
                i = i+1
            network = Network(argList[2], argList[3], argList[4], TreshholdValues, argList[5])
            patterns = load(argList[2], argList[1])

            print(patterns)
            for pattern in patterns:
                network.input(pattern)

            print("\nRESULT FOR INITIAL TRY")
            print("Sequence".rjust(5) + " Amount")
            for n in network.final_neurons:
                print(n.logo.get_motif() + " " + str(n.seq_amount))

            leftovers = network.reduce_final_outputs()

            print("\nRESULT WITHOUT REDUNDANT OUTPUTS")
            print("Sequence".rjust(5) + " Amount")
            for n in network.final_neurons:
                print(n.logo.get_motif() + " " + str(n.seq_amount))

            random.shuffle(leftovers)
            for pattern in leftovers:
                network.input(pattern)

            print("\nRESULT AFTER USING LEFTOVERS")
            print("Sequence".rjust(5) + " Amount")
            for n in network.final_neurons:
                if n.seq_amount < argList[5]:
                    continue
                print(n.logo.get_motif() + " " + str(n.seq_amount))