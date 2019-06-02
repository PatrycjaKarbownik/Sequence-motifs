import random

from FinalNeuron import FinalNeuron
from Neuron import Neuron
from input_patterns import load


def get_next_output(sequence, neurons):
    # First we need to find winning category in given neurons
    max_value = 0
    winning_output = None
    for neuron in neurons:
        match_value = neuron.calculate_matching(sequence)
        if match_value >= max_value:
            max_value = match_value
            winning_output = neuron
    return winning_output


class Network:
    first_neurons = []
    final_neurons = []
    threshold_values = []

    def __init__(self, seq_size, layers_amount, max_error, threshold_values, threshold_seq_amount):
        if layers_amount < 2:
            raise ValueError("Number of layers cannot be less than 2")
        if len(threshold_values) != layers_amount - 1:
            raise ValueError("You need threshold values for all expect of last layers")
        self.seq_size = seq_size
        self.layers_amount = layers_amount
        self.max_error = max_error
        self._create_neurons()
        self.threshold_values = threshold_values
        self.threshold_seq_amount = threshold_seq_amount

    def _create_neurons(self):
        neuron = Neuron(self.seq_size, self.first_neurons)
        self.first_neurons.append(neuron)
        actual_layer = 2
        while actual_layer != self.layers_amount:
            new_neuron = Neuron(self.seq_size, neuron)
            neuron.append_output(new_neuron)
            neuron = new_neuron
            actual_layer += 1
        new_final_neuron = FinalNeuron(self.seq_size, self.max_error, neuron)
        self.final_neurons.append(new_final_neuron)
        neuron.append_output(new_final_neuron)

    def input(self, sequence):
        """This function tells a story of sequence that lands in this very network

        95% of time network will spend on handling inputs. This is hearth of whole network, which does this:

        We start from first layer, searching for best fitting category for our sequence. When we find one, we then
        check whether it is not too distinct from this category by checking match with least matching "inner" category
        of this category. If it's smaller than our threshold value, then we need to add new categories to our network
        for this sequence. We repeat this several times until we reach our final layers (to be precise, when we're
        in layers just before final layers). We check which final layer fits best our sequence and when we choose one,
        we check if it "belongs" to this category with method belongs (which essentially just checks if number of
        mismatched letters with already assigned to this category sequences is not greater than max_error). If the
        answer is yes, then we just assign this sequence to this category. Otherwise, we create new final category for
        our sequence.
        """
        actual_layer = 1
        actual_neurons = self.first_neurons
        parent_neuron = None
        while actual_layer != self.layers_amount:
            winning_output = get_next_output(sequence, actual_neurons)
            min_value = winning_output.get_minimum_output(sequence)
            # Here we check our threshold value. If it's greater than our minimal value then we have to add
            # new categories to our network and automatically append our sequence to this new categories
            if min_value < self.threshold_values[actual_layer - 1]:
                self._append_new_neurons(actual_layer, parent_neuron, sequence)
                return
            winning_output.append_sequence(sequence)
            actual_neurons = winning_output.get_output_neurons()
            parent_neuron = winning_output
            actual_layer += 1
        # Now we're checking whether our sequence belongs to final category or we have to make another
        winning_output = get_next_output(sequence, actual_neurons)
        if winning_output.belongs(sequence):
            winning_output.append_sequence(sequence)
        else:
            new_output = FinalNeuron(self.seq_size, self.max_error, parent_neuron)
            new_output.append_sequence(sequence)
            self.final_neurons.append(new_output)
            parent_neuron.append_output(new_output)

    def _append_new_neurons(self, actual_layer, parent_neuron, sequence):
        """Append new neurons

        When we chose best fitting category (neuron) and then it won't pass our threshold value test, we need to
        create new category for this special output. We are doing this by creating new neurons for every layer
        from our parent neuron to the end. All these neurons have our sequence appended at the beginning.
        """
        while actual_layer != self.layers_amount:
            if parent_neuron is None:
                new_neuron = Neuron(self.seq_size, self.first_neurons)
                self.first_neurons.append(new_neuron)
            else:
                new_neuron = Neuron(self.seq_size, parent_neuron)
                parent_neuron.append_output(new_neuron)
            new_neuron.append_sequence(sequence)
            parent_neuron = new_neuron
            actual_layer += 1
        new_neuron = FinalNeuron(self.seq_size, self.max_error, parent_neuron)
        new_neuron.append_sequence(sequence)
        self.final_neurons.append(new_neuron)
        parent_neuron.append_output(new_neuron)

    def get_final_neurons(self):
        return self.final_neurons

    def reduce_final_outputs(self):
        recycled_sequences = []
        for neuron in self.final_neurons:
            if neuron.seq_amount < self.threshold_seq_amount:
                sequences = neuron.get_sequences()
                recycled_sequences.extend(sequences)
                sequences.clear()
                neuron.leave_parent()
        return recycled_sequences

    def draw_network(self):
        for neuron in self.first_neurons:
            self._draw_connections(neuron)

    def _draw_connections(self, node):
        if isinstance(node, Neuron):
            print("(" + node.logo.get_complex_motif() + ")" + str(len(node.output_neurons)) + " -> [ ", end='')
            for child in node.output_neurons:
                self._draw_connections(child)
            print(" ] ", end='')
        else:
            print("\"" + node + "\" ", end='')


if __name__ == "__main__":
    network = Network(5, 4, 2, [0.40, 0.6, 0.8], 3)
    patterns = load(5, "data1.txt")
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
        if n.seq_amount < 3:
            continue
        print(n.logo.get_motif() + " " + str(n.seq_amount))
