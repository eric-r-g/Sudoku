saida = [
    "    A   B   C    D   E   F    G   H   I",
    " ++---+---+---++---+---+---++---+---+---++",
    " ++===+===+===++===+===+===++===+===+===++"
    ]
lista_de_impres = [0, 1, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 0]

def saida_grade(matriz):
    cont = 0;
    for i in range(21):
        if lista_de_impres[i] < 3:
            print(saida[lista_de_impres[i]])
        else:
            print(f"{cont + 1}||{matriz[cont][0]}|{matriz[cont][1]}|{matriz[cont][2]}||{matriz[cont][3]}|{matriz[cont][4]}|{matriz[cont][5]}||{matriz[cont][6]}|{matriz[cont][7]}|{matriz[cont][8]}||{cont + 1}")
            cont += 1


matriz = [["   "] * 9] * 9
matriz[5][5] = " 7 "
saida_grade(matriz)
