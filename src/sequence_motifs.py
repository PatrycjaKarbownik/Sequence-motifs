import argparse
import sys

from Network import Network
from input_patterns import load
from Motif import Motif
import random


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
        motifs.append(Motif(n.profile.get_complex_motif(), n.profile.get_motif(), n.seq_amount))

    motifs.sort(key=lambda x: x.seq_amount, reverse=True)
    for motif in motifs:
        print("COMPLEX MOTIF: ".ljust(15) + motif.complex_motif)
        print("MOTIF: ".ljust(15) + motif.motif)
        print("AMOUNT: ".ljust(15) + str(motif.seq_amount))
        print("---------------------------------------------")


def input_to_network(network_, inputs):
    inputs_amount = len(inputs)
    counter = 0
    for pattern in inputs:
        counter += 1
        if counter % 100 == 0:
            sys.stdout.write("\rCalculation progress: {:d}/{:d}".format(counter, inputs_amount))
            sys.stdout.flush()
        network_.input(pattern)
    sys.stdout.write("\rCalculation progress: {0}/{0}".format(inputs_amount))
    sys.stdout.flush()
    print()

def sequence_size(string):
    return check_integer(string, "Size of sequence")


def layers_amount(string):
    value = check_integer(string, "Amount of layers")
    if value < 2:
        msg = "Number of layers has to be greater or equal 2"
        raise argparse.ArgumentTypeError(msg)
    return check_integer(string, "Amount of layers")


def max_error(string):
    return check_integer(string, "Maximum error")


def min_sequences(string):
    return check_integer(string, "Minimum amount of sequences")


def check_integer(string, variable_name):
    if not float(string).is_integer():
        msg = "%Value error of {0}. {1} has to be whole number".format(string, variable_name)
        raise argparse.ArgumentTypeError(msg)
    value = int(string)
    if value <= 0:
        msg = "%Value error of {0}. {1} has to greater than 0".format(string, variable_name)
        raise argparse.ArgumentTypeError(msg)
    return value


def threshold_value(string):
    if not float(string):
        msg = "Threshold values have to be numbers from 0 to 1"
        raise argparse.ArgumentTypeError(msg)
    value = float(string)
    if value < 0 or value > 1:
        msg = "Threshold values have to be numbers from 0 to 1"
        raise argparse.ArgumentTypeError(msg)
    return value


def create_parser():
    parser = argparse.ArgumentParser(description="Find motifs in given sequences")
    parser.add_argument("file_name", help="name of file with data in /data folder")
    parser.add_argument("sequence_size", type=sequence_size, help="number of nucleotides in motif")
    parser.add_argument("max_error", type=max_error,
                        help="maximum number of differences between two sequences that can be considered "
                             "as the same motif")
    parser.add_argument("-l", "--layers", default=4, type=layers_amount, metavar="amount",
                        help="number of layers of neural network "
                             "(more of them means faster work and more diverse results). It has to be at least 2")
    parser.add_argument("-m", "--min_sequences", type=min_sequences, metavar="amount", default=4,
                        help="minimum number of sequences that can be classified as motif")
    parser.add_argument("-t", "--thresholds", type=lambda s: map(threshold_value, s.split(",")), metavar="N",
                        help="values for thresholds in layers (there have to be one less than there is layers, "
                             "they also should be in ascending order, so network will categorize sequences making "
                             "with every step. They had to be separated by \",\", for example: 0.2,0.4,0.6")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="at the end of calculations print structure of network and it's motifs")
    return parser


# This function just gives linear numbers from 0.2 to 0.65 for given amount of layers
def default_thresholds(layers):
    amount = layers - 1
    maximum = 0.65
    minimum = 0.2
    difference = maximum - minimum
    quotient = difference / (amount - 1) if amount > 1 else 0
    result = [minimum]
    actual = minimum
    for i in range(amount - 2):
        actual = round(actual + quotient, 4)
        result.append(actual)
    if amount != 1:
        result.append(maximum)
    return result


def set_up_network(args_):
    seq_size_ = args_.sequence_size
    max_error_ = args_.max_error
    layers = args_.layers
    threshold_seq_amount_ = args_.min_sequences
    threshold_values = list(args_.thresholds) if isinstance(args_.thresholds, map) \
        else default_thresholds(layers)
    if len(threshold_values) >= layers:
        raise argparse.ArgumentTypeError("Too many threshold values! There should be (number of layers - 1) values.")
    network_ = Network(seq_size_, layers, max_error_, threshold_values, threshold_seq_amount_)
    return network_


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    network = set_up_network(args)
    file_name = args.file_name
    threshold_seq_amount = args.min_sequences
    seq_size = args.sequence_size
    debug_mode = args.debug

    patterns = load(seq_size, file_name)

    input_to_network(network, patterns)

    leftovers = network.reduce_final_outputs()

    random.shuffle(leftovers)

    print("Recycling and shuffling non-motifs")
    input_to_network(network, leftovers)

    if debug_mode:
        print("########## STRUCTURE OF NETWORK ##########")
        network.draw_network()

    print("\n\n########## FINAL RESULT ##########")
    print()
    draw_motifs(network.final_neurons, threshold_seq_amount)
