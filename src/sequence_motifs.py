import sys

def printHelp():
    print("Wprowadziles zle argumenty. Sprawdz czy spelniaja wymagania:")
    print("- FILE_NAME           -> nazwa pliku w cudzyslowie, na przykład: \"data2.txt\"")
    print("- SEQ_SIZE            -> dlugosc szukanych motywow (minimum 4)")
    print("- LAYERS_AMOUNT       -> liczba warstw sieci (minimum 2)")
    print("- MAX_ERROR           -> masymalna ilosc rozniacych sie znakow w motywie (minimum 0)")
    print("- TRESHHOLD_SEQ_AMOUNT-> minimalna ilosc sekwencji uznana za motyw (minimum 2)")
    print("- TRESHHOLD_VALUES    -> liczby z przedzialu <0;1> w ilosci LAYERS_AMOUNT - 1")

def checkValues(argList, count):
    if not isinstance(argList[1], str) or (argList[1].count(".txt") != 1):
        return False
    argList[2] = int(argList[2])
    if argList[2] < 4:                             # or argList[2] < 4:
        return False
    argList[3] = int(argList[3])
    if argList[3] < 2:
        return False
    argList[4] = int(argList[4])
    if argList[4] < 0:
        return False
    argList[5] = int(argList[5])
    if argList[5] < 2:
        return False
    i = 6
    while i < count:
        argList[i] = float(argList[i])
        if argList[i] < 0 or argList[i] > 1:
            return False
        i = i+1
    return True

if __name__ == "__main__":

    argList = sys.argv

    count = 5+int(argList[3])
    if len(argList) != count:
        printHelp()
    else:
        if not checkValues(argList, count):
            print("Ilosc parametrow dobra, ale zle wartosci...")
            printHelp()
        else:
            print("gites")
