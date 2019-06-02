class Motif:

    def __init__(self, complex_motif, motif, seq_amount):
        self.complex_motif = complex_motif
        self.motif = motif
        self.seq_amount = seq_amount

    def get_seq_amount(self):
        return self.seq_amount

    def get_motif(self):
        return self.motif

    def get_complex_motif(self):
        return self.complex_motif
