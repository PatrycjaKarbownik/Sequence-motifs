import numpy as np

from src.nucleotide import nucleotide_index

max_bits = 2


# TODO I am not sure whether we should keep probabilities in current form
class Logo:
    """Class that stores motif and is able to adjust dynamically"""

    def __init__(self, seq_size):
        # Bits are bits of information per nucleotide in certain spot
        self.bits = np.zeros((seq_size, 4))  #
        # counts tells us how many times certain nucleotide was in certain spot
        self.counts = np.zeros((seq_size, 4))
        # probabilities are self-explanatory
        self.probabilities = np.zeros((seq_size, 4))
        # seq_amount is amount of sequences used to build logo
        self.seq_amount = 0
        # size determines size of sequences used to build logo
        self.seq_size = seq_size

    def load_sequences(self, sequences):
        for sequence in sequences:
            self.load_sequence(sequence, False)
        self._calculate_logo()

    def load_sequence(self, sequence, recalculate=True):
        if len(sequence) != self.seq_size:
            return
        for i, char in enumerate(sequence):
            self.counts[i][nucleotide_index(char)] += 1
        self.seq_amount += 1
        if recalculate:
            self._calculate_logo()

    # TODO get rid of code duplicate
    def _calculate_logo(self):
        """This function calculates current logo based on counts of nucleotides.

        It has to be called every time user adds a sequence to logo, but because we could add multiple sequences
        at once it is not necessary to run it that many times. It should be called after every sequence is
        loaded.

        This is how it works: First we want to calculate scale of our information. Every nucleotide can carry up to
        2 bits of information (when it is the only nucleotide that showed up at certain position). However, it is not
        the case when different nucleotides were spotted at the same place. Therefore it carries less information for
        us and that is why we need to scale it. Formula for scale:
        scale = 2 + sum for every nucleotide (fn + log2(fn))
        where fn is frequency of certain nucleotide appearing at certain spot. We see that for four nucleotides showing
        the same amount of time (at the same spot) sum will be 4 * -1/2 = -2, so our scale will be 0 (since every
        nucleotide will carry exact same amount of information). Later we calculate this amount of information that \
        certain nucleotide carries with this formula:
        bits = scale * fn
        Frequency cannot be other than form 0 to 1, hence bits of information will be from 0 to 2.
        For every position in sequence we take the amount of certain nucleotides (A, T, C or G)
        that showed up at this position. At last we calculate probability of certaing nucleotide by simply
        dividing bits of information by max information (bits / 2)
        """
        for position in range(self.seq_size):
            scale = max_bits
            for nucleotide in range(4):
                counts = self.counts[position][nucleotide]
                if counts != 0:
                    frequency = counts / self.seq_amount
                    scale += (frequency * np.log2(frequency))

            for nucleotide in range(4):
                counts = self.counts[position][nucleotide]
                if counts != 0:
                    frequency = counts / self.seq_amount
                    bits = frequency * scale
                    self.bits[position][nucleotide] = bits
                    self.probabilities[position][nucleotide] = bits / max_bits


if __name__ == "__main__":
    logo = Logo(5)
    sequences = ["ATAGT", "ACGGT", "ATAGT", "ATAGT"]
    logo.load_sequences(sequences)
    print("Order: A T G C")
    print("Bits of information:")
    print(logo.bits)
    print("Probabilities:")
    print(logo.probabilities)
