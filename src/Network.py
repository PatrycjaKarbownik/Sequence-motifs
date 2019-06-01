from src.FinalNeuron import FinalNeuron
from src.Neuron import Neuron


# TODO implement input
# TODO add comments
# TODO add threshold values handling
class Network:
    first_neurons = []

    def __init__(self, seq_size, num_layers, max_error):
        if num_layers < 2:
            print("Number of layers cannot be less than 2")
        self.seq_size = seq_size
        self.num_layers = num_layers
        self.max_error = max_error
        self._create_neurons()

    def _create_neurons(self):
        neuron = Neuron(self.seq_size)
        self.first_neurons.append(neuron)
        actual_layer = 2
        while actual_layer != self.num_layers:
            new_neuron = Neuron(self.seq_size)
            neuron.append_output(new_neuron)
            neuron = new_neuron
            actual_layer += 1
        neuron.append_output(FinalNeuron(self.max_error))

    def input(self, sequence):
        pass


if __name__ == "__main__":
    Network(5, 4, 3)
