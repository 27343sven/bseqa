#!/usr/bin/python3

import os

TEST_SEQ1 = "mltaeekaavtafwgkvkvdevggealgrllvvypwtqrffesfgdlstadavmnnpkvkahgkkvldsfsngmkhlddlkgtfaalselhcdklhvdpenfkllgnvlvvvlarnfgkeftpvlqadfqkvvagvanalahryh"
TEST_SEQ2 = "mvlsaadkgnvkaawgkvgghaaeygaealermflsfpttktyfphfdlshgsaqvkghgakvaaaltkavehlddlpgalselsdlhahklrvdpvnfkllshsllvtlashlpsdftpavhasldkflanvstvltskyr"
TEST_SEQ3 = "mvhltaeekslvsglwgkvnvdevggealgrllivypwtqrffdsfgdlstpdavmsnakvkahgkkvlnsfsdglknldnlkgtfaklselhcdklhvdpenfkllgnvlvcvlahhfgkeftpqvqaayqkvvagvanalahkyh"
TEST_SEQ4 = "mvlspadktnikstwdkigghagdyggealdrtfqsfpttktyfphfdlspgsaqvkahgkkvadalttavahlddlpgalsalsdlhayklrvdpvnfkllshcllvtlachhpteftpavhasldkffaavstvltskyr"
TEST_SEQ5 = "mpivdtgsvaplsaaektkirsawapvystyetsgvdilvkfftstpaaqeffpkfkglttadqlkksadvrwhaeriinavndavasmddtekmsmklrdlsgkhaksfqvdpqyfkvlaaviadtvaagdagfeklmsmicillrsay"
TEST_SEQ6 = "mpivdtgs"
TEST_SEQ7 = "mvlspadkt"

def main():
    isGlobal, isNuc, isStandaard, matrix = keuze_menu()
    seq1, seq2 = get_sequence(isNuc)
    if isGlobal:
        make_alignment(seq1, seq2, isNuc, matrix, isGlobal)
    else:
        make_alignment(seq1, seq2, isNuc, matrix, isGlobal)
    if keuze("wilt u nog een alignment maken(1), of afsluiten(2)"):
        main()
    
    

def get_sequence(isNuc):
    isHandm = keuze("Wilt u de sequenties handmatig invoeren(1) of importeren(2)?")
    if isHandm:
        seq1 = input_sequence(isNuc, "Voer de eerste sequencie in")
        seq2 = input_sequence(isNuc, "Voer de tweede sequencie in")
    else:
        #todo
        #importeren van sequenties
        if isNuc:
            seq1, seq2 = "ATAACG", "ATCG"
        else:
            seq1, seq2 = TEST_SEQ4, TEST_SEQ7
    return(seq1.upper(), seq2.upper())

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
    isStandaard = keuze("Wilt u een standaard matrix(1) gebruiken of wilt u er één importeren(2)?")
    if not isStandaard:
        matrix = import_matrix(isNuc)
    else:
        matrix = return_matrix(isNuc)
    return(isGlobal, isNuc, isStandaard, matrix)

def keuze(text):
    print(text)
    keuze = input(":")
    while keuze not in ["1", "2", 1, 2]:
        print(type(keuze))
        print("geen geldige input.")
        keuze = input(":")
    if keuze in ["1", 1]:
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
    title_row = matrix[0]
    value = ""
    if x in title_row and y in title_row:
        for i in range(len(matrix)):
            if x != 0:
                if matrix[i][0] == x:
                    value = matrix[i][title_row.index(y) + 1]
    else:
        print("gegeven waardes staan niet in de matrix!")
        return(0)
    if not is_int(value):
        print("er zit een fout in de matrix!, kon geen int maken van matrix waarde")
        return(0)
    return(value)

def print_table(seq1, seq2, table):
    test_table = table
    if len(seq1) + 1 == len(test_table) and len(seq2) + 1 == len(test_table[0]):
        test_table = [[" "] + list(seq2)] + test_table
        for x in range(len(test_table)):
            if x < 2:
                test_table[x] = [" "] + test_table[x]
            else:
                test_table[x] = [seq1[x-2]] + test_table[x]
        inverted_table = invert_table(test_table)
        for x in range(len(inverted_table)):
            length = get_max_row_length(inverted_table[x])
            for y in range(len(inverted_table[x])):
                inverted_table[x][y] = inverted_table[x][y].ljust(length + 2)
        test_table = invert_table(inverted_table)
        for x in test_table:
            print("".join(x))
    else:
        print("gegeven sequenties komen niet overeen met de tabel")
    return(test_table)
        

def get_max_row_length(row):
    length = 0
    for x in row:
        if len(str(x)) > length:
            length = len(str(x))
    return(length)

def invert_table(table):
    new_table = []
    for x in range(len(table[0])):
        new_row = []
        for y in range(len(table)):
            new_row.append(table[y][x])
        new_table.append(new_row)
    return(new_table)

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

def make_alignment(seq1, seq2, isNuc, matrix, isGlobal):
    table = make_table(seq1, seq2, matrix, isGlobal)
    table = fill_table(seq1, seq2, matrix, table, isGlobal)
    info = print_table(seq1, seq2, table)
    end = False
    x, y, new_seq1, new_seq2 = 0, 0, "", ""
    if not isGlobal:
        hoogste = 0
        for test_x in range(len(table)):
            for test_y in range(len(table[test_x])):
                if int(table[test_x][test_y].split("]")[1]) > hoogste:
                    hoogste = int(table[test_x][test_y].split("]")[1])
                    x, y = test_x, test_y
        test_x, test_y = x, y
    else:
        x, y = len(seq1), len(seq2)
    count = 0
    while end == False:
        direction = table[x][y].split("[")[1].split("]")[0]
        if len(direction) == 1:
            if direction == "|":
                new_seq1 += seq1[x-1]
                new_seq2 += "_"
                x -= 1
            elif direction == "\\":
                new_seq1 += seq1[x-1]
                new_seq2 += seq2[y-1]
                x -= 1
                y -= 1
            elif direction == "-":
                new_seq1 += "_"
                new_seq2 += seq2[y-1]
                y -= 1
            elif direction == "0":
                end = True
            else:
                print("er heeft zich een fout voorgedaan in de traceback")
                end = True
        else:
            
            value_list = []
            sign_list = []
            for z in direction:
                if z == "|":
                    value_list.append(int(table_value(x-1, y, table)))
                    sign_list.append("|")
                elif z == "\\":
                    value_list.append(int(table_value(x-1, y-1, table)))
                    sign_list.append("\\")
                elif z == "-":
                    value_list.append(int(table_value(x, y-1, table)))
                    sign_list.append("-")
                else:
                    print("er heeft zich een fout voorgedaan in (multiple) traceback")
            index = value_list.index(max(value_list))
            if value_list.count(max(value_list)) > 1:
                count += 1
            if sign_list[index] == "-":
                new_seq1 += "_"
                new_seq2 += seq2[y-1]
                y -= 1
            if sign_list[index] == "\\":
                new_seq1 += seq1[x-1]
                new_seq2 += seq2[y-1]
                x -= 1
                y -= 1
            if sign_list[index] == "|":
                new_seq1 += seq1[x-1]
                new_seq2 += "_"
                x -= 1
    print(new_seq1[::-1])
    print(new_seq2[::-1])
    if not isGlobal:
        print("de hoogste alignment score is", hoogste, "op de coordinaten", test_x, test_y)
    print("er waren", count, "momenten in de traceback waar twee opties even goed waren.")
    print("alignment wordt opgeslagen in alignment.csv")
    file = open("alignment.csv", "w")
    for x in info:
        file.write(";".join(x) + "\n")
    file.close()  

def fill_table(seq1, seq2, matrix, table, isGlobal):
    for y in range(len(seq2)):
        for x in range(len(seq1)):
            dir_str = ""
            possible_ways = [int(table_value(x+1, y, table)) + int(search_in_matrix("*", "A", matrix)),
                             int(table_value(x, y, table)) + int(search_in_matrix(seq2[y], seq1[x], matrix)),
                             int(table_value(x, y+1, table)) + int(search_in_matrix("*", "A", matrix))]
            if not isGlobal:
                possible_ways.append(0)
            hoogste = max(possible_ways)
            if possible_ways[0] == hoogste:
                dir_str += "-"
            if possible_ways[1] == hoogste:
                dir_str += "\\"
            if possible_ways[2] == hoogste:
                dir_str += "|"
            if not isGlobal and possible_ways[3] == hoogste:
                dir_str = "0"
            table[x+1][y+1] = "[" + dir_str + "]" + str(hoogste)
    return(table)

def table_value(x, y, table):
    try:
        test = table[x][y].split("]")[1]
    except IndexError:
        print("x:", x, "y:", y)
    return(table[x][y].split("]")[1])

def make_table(seq1, seq2, matrix, isGlobal):
    new_table, first_row, current_value = [], [], 0
    gap_waarde = int(search_in_matrix("*", "A", matrix))
    for x in range(len(seq2) + 1):
        if x != 0:
            if not isGlobal:
                first_row.append("[0]0")
            else:
                first_row.append("[-]" + str(current_value))
        else:
            first_row.append("[0]" + str(current_value))
        current_value += gap_waarde
    new_table.append(first_row)
    current_value = gap_waarde
    for x in range(len(seq1)):
        if not isGlobal:
            new_table.append(["[0]0"] + [""] * len(seq2))
        else:
            new_table.append(["[|]" + str(current_value)] + [""] * len(seq2))
            current_value += gap_waarde
    return(new_table)
       

main()
