# PSZT_Sequence_motifs
Finding motifs using kohonen's neural network (self-organized map)

## Authors:
Karbownik Patrycja https://github.com/PatrycjaKarbownik <br>
Aksamit Sebastian https://github.com/Temebe <br>
Grabowski Kamil https://github.com/Nestus97

## Task:
Create neural network, which finds motifs from DNA sequences.

### Execute:
python3 *sequence_motifs.py* <FILE_NAME> <SEQ_SIZE> <LAYERS_AMOUNT> <MAX_ERROR> <THRESHOLD_SEQ_AMOUNT> <THRESHOLD_VALUES>

FILE_NAME -> file with sequences, for example: "data2.txt" <br>
SEQ_SIZE            -> motifs' length (minimum 4) <br>
LAYERS_AMOUNT       -> how many layers the network will have (minimum 2) <br>
MAX_ERROR           -> max number of nucleotides differences in motif (minimum 0) <br>
THRESHOLD_SEQ_AMOUNT-> minimum number of sequences which decide if it is a motif (minimum 2) <br>
THRESHOLD_VALUES    -> (LAYERS_AMOUNT - 1) float numbers between 0 and 1 

e.g. <br>
python3 sequence_motifs.py "data2.txt" 5 3 5 4 0.2 0.4
