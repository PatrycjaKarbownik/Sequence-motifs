import random
import sys

from Network import Network
from Neuron import Neuron
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
        iterator = iterator + 1
    return True


def draw_motifs(neurons, minimal_seq_amount):
    motifs = []
    for n in neurons:
        if n.seq_amount < minimal_seq_amount:
            continue
        motifs.append(Motif(n.logo.get_complex_motif(), n.logo.get_motif(), n.seq_amount))

    motifs.sort(key=lambda x: x.seq_amount, reverse=True)
    for motif in motifs:
        print("COMPLEX MOTIF: ".ljust(15) + motif.complex_motif)
        print("MOTIF: ".ljust(15) + motif.motif)
        print("AMOUNT: ".ljust(15) + str(motif.seq_amount))
        print("---------------------------------------------")


def set_up():
    arg_list = sys.argv
    if len(arg_list) < 4 or len(arg_list) != 5 + int(arg_list[3]):
        print_help()
        return False, None, None, None, None, None, None
    try:
        file_name = arg_list[1]
        seq_size = int(arg_list[2])
        layers_amount = int(arg_list[3])
        max_error = int(arg_list[4])
        threshold_seq_amount = int(arg_list[5])
        threshold_values = []
        count = 5 + int(arg_list[3])
        i = 2
        while i < 6:
            arg_list[i] = int(arg_list[i])
            i = i + 1
        while i < count:
            arg_list[i] = float(arg_list[i])
            i = i + 1
        if not check_values(arg_list, count):
            print("Program received wrong")
            print_help()
            return False, None, None, None, None, None, None
        else:
            i = 6
            while i < count:
                threshold_values.append(arg_list[i])
                i = i + 1
    except (ValueError, TypeError):
        print("Wrong values")
        print_help()
        return False, None, None, None, None, None, None
    return True, file_name, seq_size, layers_amount, max_error, threshold_seq_amount, threshold_values


if __name__ == "__main__":
    set_up_successful, file_name, seq_size, layers_amount, max_error, threshold_seq_amount, threshold_values = set_up()
    if not set_up_successful:
        sys.exit("Wrong arguments")
    network = Network(seq_size, layers_amount, max_error, threshold_values, threshold_seq_amount)
    patterns = load(seq_size, file_name)

    # print(patterns)
    for pattern in patterns:
        network.input(pattern)

    print("########## INITIAL NETWORK ##########")
    network.draw_network()

    print("\n\n########## RESULT FOR INITIAL TRY ##########")
    draw_motifs(network.final_neurons, 0)

    leftovers = network.reduce_final_outputs()

    print("\n\n########## RESULT WITHOUT REDUNDANT OUTPUTS ##########")
    draw_motifs(network.final_neurons, 0)

    random.shuffle(leftovers)
    for pattern in leftovers:
        network.input(pattern)

    print("\n\n########## FINAL NETWORK ##########")
    network.draw_network()

    print("\n\n########## FINAL RESULT ##########")
    print()
    draw_motifs(network.final_neurons, threshold_seq_amount)
