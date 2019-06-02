from Logo import Logo


class Neuron:

    # It is important that parent may not be neuron. If neuron is in first layer than it's parent is just array
    def __init__(self, seq_size, parent):
        self.logo = Logo(seq_size)
        self.seq_size = seq_size
        self.parent = parent
        self.output_neurons = []

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

    # TODO get rid of this non-pythonic method
    def get_output_neurons(self):
        return self.output_neurons

    @NotImplementedError
    # TODO At this moment this function is unusable. It has to be rewritten
    def leave_parent(self):
        """Removing neuron from it's parent output

        This method is necessary because when we want to get rid of neuron (because i.e. final neuron doesn't meet the
        requirements for being motif) we need to inform it's parent neuron (or array) to remove this object. The reason
        why it is method in Neuron and not in FinalNeuron is that if FinalNeuron happens to be the only output neuron
        of Neuron, then there is no point of keeping this neuron (and therefore we recursively remove neurons with
        empty outputs.
        """
        if isinstance(self.parent, Neuron):
            self.parent.output_neurons.remove(self)
            if len(self.parent.output_neurons) == 0:
                self.parent.leave_parent()
        else:
            # We need to check whether we're about to remove the only one neuron from network's first layer
            # It is extremely unlikely but may happen. In this situation we simply clear neuron's logo (by creating new)
            if len(self.parent) == 1:
                self.logo = Logo(self.seq_size)
            else:
                self.parent.remove(self)


if __name__ == "__main__":
    pass
