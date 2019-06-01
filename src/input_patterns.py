import random
import sys


# load subsequences from data file - division sequences to subsequences with the same length = size_of_motifs
def load(size_of_motifs, fileName):
    input_patterns = []
    with open("../data/" + fileName, "r") as file:
        for i, line in enumerate(file):
            sequence = line.rstrip('\n')
            for begin in range(len(sequence) - size_of_motifs + 1):
                subsequence = ""
                for nucleotide_index in range(size_of_motifs):
                    subsequence += sequence[begin + nucleotide_index]
                input_patterns.append(subsequence)
    file.close()
    random.shuffle(input_patterns)
    return input_patterns


if __name__ == "__main__":
    size_of_motifs = int(input("Size of motifs: "))
    input_patterns = []

    argList = sys.argv
    load(size_of_motifs, argList[1])

    # for i in argList:
    #    print(i)

    print(input_patterns)
    random.shuffle(input_patterns)
    print(input_patterns)
