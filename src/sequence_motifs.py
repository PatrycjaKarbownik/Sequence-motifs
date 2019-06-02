import random
import sys

from Network import Network
from input_patterns import load


def printHelp():
    print("Wprowadziles zle argumenty. Sprawdz czy spelniaja wymagania:")
    print("- FILE_NAME           -> nazwa pliku w cudzyslowie, na przykład: \"data2.txt\"")
    print("- SEQ_SIZE            -> dlugosc szukanych motywow (minimum 4)")
    print("- LAYERS_AMOUNT       -> liczba warstw sieci (minimum 2)")
    print("- MAX_ERROR           -> masymalna ilosc rozniacych sie znakow w motywie (minimum 0)")
    print("- TRESHHOLD_SEQ_AMOUNT-> minimalna ilosc sekwencji uznana za motyw (minimum 2)")
    print("- TRESHHOLD_VALUES    -> liczby z przedzialu <0;1> w ilosci LAYERS_AMOUNT - 1")


def checkValues(argList, count):
    if not isinstance(argList[1], str) or (argList[1].count(".txt") != 1):
        return False
    if argList[2] < 4:                             # or argList[2] < 4:
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
            print("Ilosc parametrow dobra, ale zle wartosci...")
            printHelp()
        else:
            print("gites")
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