class Motif:
    """Class that stores motif's attributes

    This class is used to store information about motif:
    motif sequence, which is a sequence with the most likely nucleotides,
    motif with all possible nucleotides (sections separated by brackets)
    and number of sequences which are represented by motif.
    """
    def __init__(self, complex_motif, motif, seq_amount):
        self.complex_motif = complex_motif
        self.motif = motif
        self.seq_amount = seq_amount
