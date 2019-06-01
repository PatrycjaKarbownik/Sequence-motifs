class FinalNeuron:
    """Final neuron which has raw sequences

    This neuron is different because we compare here not the logos based on probability but sequences."""
    outputs = []

    def __init__(self, max_error):
        print("Creating final neuron with max_error value " + str(max_error))
        self.max_error = max_error

    def append_output(self, sequence):
        self.outputs.append(sequence)

    def belongs(self, sequence):
        for output in self.outputs:
            error = 0
            for nucleotide_a, nucleotide_b in zip(output, sequence):
                if nucleotide_a != nucleotide_b:
                    error += 1
                if error > self.max_error:
                    return False
        return True


if __name__ == "__main__":
    sequence_a = "ATAGTA"
    sequence_b = "ATACTA"
    sequence_c = "ATAGCA"
    sequence_d = "ATAGGA"
    sequence_e = "ATGCCA"
    final_neuron = FinalNeuron(2)
    final_neuron.append_output(sequence_a)
    final_neuron.append_output(sequence_b)
    final_neuron.append_output(sequence_c)
    print(final_neuron.belongs(sequence_d))
    print(final_neuron.belongs(sequence_e))
