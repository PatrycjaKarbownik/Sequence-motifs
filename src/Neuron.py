from src.Logo import Logo


class Neuron:
    output_neurons = []

    def __init__(self, seq_size):
        print("Creating neuron of size " + str(seq_size))
        self.logo = Logo(seq_size)

    def calculate_matching(self, sequence):
        return self.logo.calculate_matching(sequence)

    def append_sequence(self, sequence):
        self.logo.load_sequence(sequence)

    def append_output(self, neuron):
        self.output_neurons.append(neuron)

    def get_minimum_output(self, sequence):
        """Calculating minimal matching value in output neurons

        This function takes all of its outputs and calculates how similar the sequence is to this outputs.
        We're searching for the least matching output category. Later network based on this minimal value will
        assign new sequence to this neuron OR (if threshold value will be grater than minimal matching value) it will
        create new neuron for this sequence.

        """
        min_value = 1
        for output in self.output_neurons:
            match = output.calculate_matching(sequence)
            min_value = match if match < min_value else min_value
        return min_value

    def get_output_neurons(self):
        return self.output_neurons


if __name__ == "__main__":
    pass
