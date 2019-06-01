from src.FinalNeuron import FinalNeuron
from src.Neuron import Neuron


# TODO implement input
# TODO add comments
# TODO add threshold values handling
def get_next_output(sequence, neurons):
    # First we need to find winning category in given neurons
    max_value = 0
    winning_output = None
    for neuron in neurons:
        match_value = neuron.calculate_matching(sequence)
        if match_value > max_value:
            max_value = match_value
            winning_output = neuron
    return winning_output


class Network:
    first_neurons = []
    threshold_values = []

    def __init__(self, seq_size, layers_amount, max_error, threshold_values):
        if layers_amount < 2:
            raise ValueError("Number of layers cannot be less than 2")
        if len(threshold_values) != layers_amount - 1:
            raise ValueError("You need threshold values for all expect of last layers")
        self.seq_size = seq_size
        self.layers_amount = layers_amount
        self.max_error = max_error
        self._create_neurons()
        self.threshold_values = threshold_values

    def _create_neurons(self):
        neuron = Neuron(self.seq_size)
        self.first_neurons.append(neuron)
        actual_layer = 2
        while actual_layer != self.layers_amount:
            new_neuron = Neuron(self.seq_size)
            neuron.append_output(new_neuron)
            neuron = new_neuron
            actual_layer += 1
        neuron.append_output(FinalNeuron(self.seq_size, self.max_error))

    def input(self, sequence):
        actual_layer = 1
        actual_neurons = self.first_neurons
        parent_neuron = None
        while actual_layer != self.layers_amount:
            winning_output = get_next_output(sequence, actual_neurons)
            min_value = winning_output.get_minimum_output(sequence)
            if min_value < self.threshold_values[actual_layer - 1]:
                self._append_new_neurons(actual_layer, parent_neuron, sequence)
        pass

    def _append_new_neurons(self, actual_layer, parent_neuron, sequence):
        if parent_neuron is None:
            parent_neuron = self.first_neurons
        while actual_layer != self.layers_amount:
            new_neuron = Neuron(self.seq_size)
            new_neuron.append_sequence(sequence)
            parent_neuron.append_output(new_neuron)
            parent_neuron = new_neuron


if __name__ == "__main__":
    Network(5, 4, 3, [0.40, 0.6, 0.8])
