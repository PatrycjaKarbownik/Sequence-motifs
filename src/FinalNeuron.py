from src.Neuron import Neuron


class FinalNeuron(Neuron):
    """Final neuron which has raw sequences

    This neuron is different because we compare here not the logos based on probability but sequences."""
    output_neurons = []
    seq_amount = 0

    def __init__(self, seq_size, max_error, parent_array):
        super().__init__(seq_size)
        print("Creating final neuron with max_error value " + str(max_error))
        self.max_error = max_error
        self.parent_array = parent_array

    # We're additionally adding whole sequence to our output's list instead of just adding to logo
    def append_sequence(self, sequence):
        super().append_sequence(sequence)
        self.output_neurons.append(sequence)
        self.seq_amount += 1

    def belongs(self, sequence):
        for output in self.output_neurons:
            error = 0
            for nucleotide_a, nucleotide_b in zip(output, sequence):
                if nucleotide_a != nucleotide_b:
                    error += 1
                if error > self.max_error:
                    return False
        return True

    def get_sequences(self):
        return self.output_neurons

    def leave_parent(self):
        self.parent_array.remove(self)


if __name__ == "__main__":
    sequence_a = "ATAGTA"
    sequence_b = "ATACTA"
    sequence_c = "ATAGCA"
    sequence_d = "ATAGGA"
    sequence_e = "ATGCCA"
    final_neuron = FinalNeuron(6, 2, None)
    final_neuron.append_output(sequence_a)
    final_neuron.append_output(sequence_b)
    final_neuron.append_output(sequence_c)
    print(final_neuron.belongs(sequence_d))
    print(final_neuron.belongs(sequence_e))
