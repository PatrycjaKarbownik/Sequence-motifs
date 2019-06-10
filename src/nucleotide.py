# Nucleotides codes
A = 0
C = 1
T = 2
G = 3


def nucleotide_index(nucleotide_string):
    if nucleotide_string == "A":
        return A
    if nucleotide_string == "T":
        return T
    if nucleotide_string == "G":
        return G
    if nucleotide_string == "C":
        return C


def nucleotide_letter(value):
    if value == A:
        return "A"
    if value == C:
        return "C"
    if value == T:
        return "T"
    if value == G:
        return "G"
