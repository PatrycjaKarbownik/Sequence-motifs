import random
import sys

from Network import Network
from input_patterns import load
from Motif import Motif
import random

def print_help():
    print("................................................................................................")
    print("Wrong arguments. Check if they meet reguirements:                                              |")
    print("- FILE_NAME           -> file with sequences, for example: \"data2.txt\"                         |")
    print("- SEQ_SIZE            -> motifs' length (minimum 4)                                            |")
    print("- LAYERS_AMOUNT       -> how many layers the network will have (minimum 2)                     |")
    print("- MAX_ERROR           -> max number of nucleotides differences in motif (minimum 0)            |")
    print("- THRESHOLD_SEQ_AMOUNT-> minimum number of sequences which decide if it is a motif (minimum 2) |")
    print("- THRESHOLD_VALUES    -> (LAYERS_AMOUNT - 1) float numbers between 0 and 1                     |")
    print("------------------------------------- EXAMPLE --------------------------------------------------")
    print("|                                                                                              |")
    print("|                python sequence_motifs.py \"data2.txt\" 5 3 5 4 0.2 0.4                         |")
    print("|                                                                                              |")
    print("------------------------------------------------------------------------------------------------")

def check_values(arg_list, count):
    if not isinstance(arg_list[1], str) or (arg_list[1].count(".txt") != 1):
        return False
    if arg_list[2] < 4:
        return False
    if arg_list[3] < 2:
        return False
    if arg_list[4] < 0:
        return False
    if arg_list[5] < 2:
        return False
    iterator = 6
    while iterator < count:
        if arg_list[iterator] < 0 or arg_list[iterator] > 1:
            return False
        iterator = iterator+1
    return True

if __name__ == "__main__":
    arg_list = sys.argv
    if len(arg_list) < 4 or len(arg_list) != 5+int(arg_list[3]):
        print()
        print_help()
    else:
        count = 5 + int(arg_list[3])
        i = 2
        while i < 6:
            arg_list[i] = int(arg_list[i])
            i = i+1
        while i < count:
            arg_list[i] = float(arg_list[i])
            i = i+1
        if not check_values(arg_list, count):
            print("................................................................................................")
            print("Number of arguments good, but wrong values...                                                  |")
            print_help()
        else:
            threshold_values = []
            i = 6
            while i < count:
                threshold_values.append(arg_list[i])
                i = i+1
            network = Network(arg_list[2], arg_list[3], arg_list[4], threshold_values, arg_list[5])
            patterns = load(arg_list[2], arg_list[1])

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

            print("\nRESULT AFTER USING LEFTOVERS:")
            print()
            #print("MOTIF".ljust(arg_list[2]) + " AMOUNT")
            motifs = []
            for n in network.final_neurons:
                if n.seq_amount < arg_list[5]:
                    continue
                
                motifs.append(Motif(n.logo.get_complex_motif(), n.logo.get_motif(), n.seq_amount))

            motifs.sort(key=lambda x: x.seq_amount, reverse=True)
            for motif in motifs:
                print("COMPLEX MOTIF: ".ljust(15) + motif.complex_motif)
                print("MOTIF: ".ljust(15) + motif.motif)
                print("AMOUNT: ".ljust(15) + str(motif.seq_amount))
                print("---------------------------------------------")
            

                

