# load subsequences from data file - division sequences to subsequences with the same length = size_of_motifs
def load(size_of_motifs):
    with open("../data/data2.txt", "r") as file:
        for i, line in enumerate(file):
            sequence = line.rstrip('\n')
            for begin in range(len(sequence) - size_of_motifs + 1):
                subsequence = ""
                for nucleotide_index in range(size_of_motifs):
                    subsequence += sequence[begin + nucleotide_index]
                input_patterns.append(subsequence)

    file.close()


if __name__ == "__main__":
    size_of_motifs = int(input("Size of motifs: "))
    input_patterns = []
    load(size_of_motifs)

    print(input_patterns)