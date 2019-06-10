# PSZT_Sequence_motifs
Finding motifs using kohonen's neural network (self-organized map)

## Authors:
Karbownik Patrycja https://github.com/PatrycjaKarbownik <br>
Aksamit Sebastian https://github.com/Temebe <br>
Grabowski Kamil https://github.com/Nestus97

## Task:
Create neural network, which finds motifs from DNA sequences.

### Execute:
python3 *sequence_motifs.py* <FILE_NAME> <SEQ_SIZE> <MAX_ERROR> <MIN_SEQUENCES> [<OPTIONAL_PARAMETERS>]

| Flags | Parametets | Meaning | Default value |
| ------ | ------ | ------ | ------ |
|-|<FILE_NAME>,<br> file has to be in "data" folder| Name of file with sequences.| - |
|-|<SEQ_SIZE>,<br> integer number | Number of nucleotides in finding motifs | - |
|-|<MAX_ERROR>,<br> integer number | Maximum number of differences between two sequences that can be considered as the same motif. | - |
|-|<MIN_SEQUENCES>,<br> integer number | Minimum number of sequences that can be classified as motif | - |
| -h<br>--help| - | Shows help | - |
| -l<br>--layers_amount | <integer_number>,<br>minimal value: 2 | Number of layers of neural network (more of them means faster work and more diverse results). It has to be at least 2 | 4 |
| -t<br>--thresholds | <numbers_from_0_to_1>,<br>separated by comma. there have to be one less than there is layers, they also should be in ascending order |  Thresholds value for each layer of neural network - determine minimal similarity between sequence and motif | From 0.2 to 0.65, linear growth |

e.g. <br>
python3 sequence_motifs.py "data1.txt" 5 3 5 4 0.2 0.4 <br>
python3 sequence_motifs.py "data1.txt" 7 4 3 5 0.4 0.6 0.8 <br>
python3 sequence_motifs.py "data3.txt" 13 6 5 5 0.1 0.35 0.5 0.6 0.7 <br>
python3 sequence_motifs.py "data3.txt" 15 2 4 <br>
