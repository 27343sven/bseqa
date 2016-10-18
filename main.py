#!/usr/bin/python3

import os

def main():
    isGlobal, isNuc, isStandaard, matrix = keuze_menu()
    seq1, seq2 = get_sequence(isNuc)
    make_global_alignment(seq1, seq2, isNuc, matrix)
    
    

def get_sequence(isNuc):
    isHandm = keuze("Wilt u de sequenties handmatig invoeren(1) of importeren(2)?")
    if isHandm:
        seq1 = input_sequence(isNuc, "Voer de eerste sequencie in")
        seq2 = input_sequence(isNuc, "Voer de tweede sequencie in")
    else:
        #todo
        #importeren van sequenties
        if isNuc:
            seq1, seq2 = "ATCG", "ATCG"
        else:
            seq1, seq2 = "HIMSTB", "HIRPMS"
    return(seq1, seq2)

def input_sequence(isNuc, text):
    print(text)
    if isNuc:
        seq = input(":")
        while seq.upper().strip("ATCG") != "":
            print("invalid sequence")
            seq = input(":")
    else:
        seq = input(":")
        while seq.upper().strip("ARNDCQEGHILKMFPSTWYVBZX") != "":
            print("invalid sequence")
            seq = input(":")
    return(seq.upper())
            
            

def keuze_menu():
    print("Welkom bij mijn alignment programma!")
    isGlobal = keuze("Wilt u een global(1) of een local(2) alignment maken?")
    isNuc = keuze("alignment met nucleotiden(1) of met peptiden(2)?")
    isStandaard = keuze("Wilt u een standaard matrix(1) gebruiken of een importeren(2)?")
    if not isStandaard:
        matrix = import_matrix(isNuc)
    else:
        matrix = return_matrix(isNuc)
    return(isGlobal, isNuc, isStandaard, matrix)

def keuze(text):
    print(text)
    keuze = input(":")
    while keuze not in ["1", "2"]:
        print("geen geldige input.")
        keuze = input(":")
    if keuze == "1":
        return(True)
    else:
        return(False)

def process_matrix(fileName):
    """
    regels voor de file zijn:
    - # worden niet meegenomen
    - de eerste rij en kolom zijn de afkortingen voor de peptiden of
      nucleotiden in hoofdletters
    - alles wordt geseparate door spaces
    """
    matrix = open(fileName, "r").readlines()
    current_index = 0
    while current_index < len(matrix):
        if matrix[current_index] != "":
            if matrix[current_index][0] == "#":
                matrix.remove(matrix[current_index])
            else:
                matrix[current_index] = [x for x in  matrix[current_index].replace("\n", "").split() if x != ""]
                current_index += 1
    print(matrix)
    return(matrix)
    
def is_int(number):
    try:
        int(number)
        return(True)
    except ValueError:
        return(False)
    
def return_matrix(isNuc):
    if isNuc:
        return([[     "A", "T", "C", "G", "*"],
                ["A", "5", "-4", "-4", "0", "-5"],
                ["T", "-4", "5", "0", "-4", "-5"],
                ["C", "-4", "0", "5", "-4", "-5"],
                ["G", "0", "-4", "-4", "5", "-5"],
                ["*", "-5", "-5", "-5", "-5", "-5"]])
    else:
        return([['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z', 'X', '*'], ['A', '4', '-1', '-2', '-2', '0', '-1', '-1', '0', '-2', '-1', '-1', '-1', '-1', '-2', '-1', '1', '0', '-3', '-2', '0', '-2', '-1', '0', '-4'], ['R', '-1', '5', '0', '-2', '-3', '1', '0', '-2', '0', '-3', '-2', '2', '-1', '-3', '-2', '-1', '-1', '-3', '-2', '-3', '-1', '0', '-1', '-4'], ['N', '-2', '0', '6', '1', '-3', '0', '0', '0', '1', '-3', '-3', '0', '-2', '-3', '-2', '1', '0', '-4', '-2', '-3', '3', '0', '-1', '-4'], ['D', '-2', '-2', '1', '6', '-3', '0', '2', '-1', '-1', '-3', '-4', '-1', '-3', '-3', '-1', '0', '-1', '-4', '-3', '-3', '4', '1', '-1', '-4'], ['C', '0', '-3', '-3', '-3', '9', '-3', '-4', '-3', '-3', '-1', '-1', '-3', '-1', '-2', '-3', '-1', '-1', '-2', '-2', '-1', '-3', '-3', '-2', '-4'], ['Q', '-1', '1', '0', '0', '-3', '5', '2', '-2', '0', '-3', '-2', '1', '0', '-3', '-1', '0', '-1', '-2', '-1', '-2', '0', '3', '-1', '-4'], ['E', '-1', '0', '0', '2', '-4', '2', '5', '-2', '0', '-3', '-3', '1', '-2', '-3', '-1', '0', '-1', '-3', '-2', '-2', '1', '4', '-1', '-4'], ['G', '0', '-2', '0', '-1', '-3', '-2', '-2', '6', '-2', '-4', '-4', '-2', '-3', '-3', '-2', '0', '-2', '-2', '-3', '-3', '-1', '-2', '-1', '-4'], ['H', '-2', '0', '1', '-1', '-3', '0', '0', '-2', '8', '-3', '-3', '-1', '-2', '-1', '-2', '-1', '-2', '-2', '2', '-3', '0', '0', '-1', '-4'], ['I', '-1', '-3', '-3', '-3', '-1', '-3', '-3', '-4', '-3', '4', '2', '-3', '1', '0', '-3', '-2', '-1', '-3', '-1', '3', '-3', '-3', '-1', '-4'], ['L', '-1', '-2', '-3', '-4', '-1', '-2', '-3', '-4', '-3', '2', '4', '-2', '2', '0', '-3', '-2', '-1', '-2', '-1', '1', '-4', '-3', '-1', '-4'], ['K', '-1', '2', '0', '-1', '-3', '1', '1', '-2', '-1', '-3', '-2', '5', '-1', '-3', '-1', '0', '-1', '-3', '-2', '-2', '0', '1', '-1', '-4'], ['M', '-1', '-1', '-2', '-3', '-1', '0', '-2', '-3', '-2', '1', '2', '-1', '5', '0', '-2', '-1', '-1', '-1', '-1', '1', '-3', '-1', '-1', '-4'], ['F', '-2', '-3', '-3', '-3', '-2', '-3', '-3', '-3', '-1', '0', '0', '-3', '0', '6', '-4', '-2', '-2', '1', '3', '-1', '-3', '-3', '-1', '-4'], ['P', '-1', '-2', '-2', '-1', '-3', '-1', '-1', '-2', '-2', '-3', '-3', '-1', '-2', '-4', '7', '-1', '-1', '-4', '-3', '-2', '-2', '-1', '-2', '-4'], ['S', '1', '-1', '1', '0', '-1', '0', '0', '0', '-1', '-2', '-2', '0', '-1', '-2', '-1', '4', '1', '-3', '-2', '-2', '0', '0', '0', '-4'], ['T', '0', '-1', '0', '-1', '-1', '-1', '-1', '-2', '-2', '-1', '-1', '-1', '-1', '-2', '-1', '1', '5', '-2', '-2', '0', '-1', '-1', '0', '-4'], ['W', '-3', '-3', '-4', '-4', '-2', '-2', '-3', '-2', '-2', '-3', '-2', '-3', '-1', '1', '-4', '-3', '-2', '11', '2', '-3', '-4', '-3', '-2', '-4'], ['Y', '-2', '-2', '-2', '-3', '-2', '-1', '-2', '-3', '2', '-1', '-1', '-2', '-1', '3', '-3', '-2', '-2', '2', '7', '-1', '-3', '-2', '-1', '-4'], ['V', '0', '-3', '-3', '-3', '-1', '-2', '-2', '-3', '-3', '3', '1', '-2', '1', '-1', '-2', '-2', '0', '-3', '-1', '4', '-3', '-2', '-1', '-4'], ['B', '-2', '-1', '3', '4', '-3', '0', '1', '-1', '0', '-3', '-4', '0', '-3', '-3', '-2', '0', '-1', '-4', '-3', '-3', '4', '1', '-1', '-4'], ['Z', '-1', '0', '0', '1', '-3', '3', '4', '-2', '0', '-3', '-3', '1', '-1', '-3', '-1', '0', '-1', '-3', '-2', '-2', '1', '4', '-1', '-4'], ['X', '0', '-1', '-1', '-1', '-2', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-2', '0', '0', '-2', '-1', '-1', '-1', '-1', '-1', '-4'], ['*', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '-4', '1']])

def search_in_matrix(x, y, matrix):
    title_row = matrix.pop(0)
    value = ""
    if x in title_row and y in title_row:
        for i in matrix:
            if i[0] == x:
                value = i[title_row.index(y) + 1]
    else:
        print("gegeven waardes staan niet in de matrix!")
        return(0)
    if not is_int(value):
        print("er zit een fout in de matrix!, kon geen int maken van matrix waarde")
        return(0)
    return(value)
        
               

def import_matrix(isNuc):
    fileName = ""
    while fileName == "":
        print("voer een bestandsnaam in.")
        fileName = input(":")
        if not os.path.isfile(fileName):
            print("Bestand bestaat niet.")
            fileName = ""
    if isNuc:
        matrix = process_matrix(fileName)
    else:
        matrix = process_matrix(fileName)
    return(matrix)

def make_global_alignment(seq1, seq2, isNuc, matrix):
    new_table, first_row, current_value = [], [], 0
    gap_waarde = int(search_in_matrix("*", "A", matrix))
    for x in range(len(seq2) + 1):
        if x != 0:
            first_row.append("[-]" + str(current_value))
        else:
            first_row.append(str(current_value))
        current_value += gap_waarde
    new_table.append(first_row)
    current_value = gap_waarde
    for x in range(len(seq1)):
        new_table.append(["[|]" + str(current_value)] + [""] * len(seq1))
        current_value += gap_waarde
    for x in new_table:
        print(x)
       

main()
