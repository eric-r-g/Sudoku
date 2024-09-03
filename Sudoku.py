saida = [
    "    A   B   C    D   E   F    G   H   I",
    " ++---+---+---++---+---+---++---+---+---++",
    " ++===+===+===++===+===+===++===+===+===++"
    ]
lista_de_impres = [0, 1, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 0]

# Função para receber a entrada e retornar o que for necessário
    # Aqui dentro vai ter a leitura do arquivo provavelmente, talvez seja interessante alguém para isso já que a função é complicada por si só

# Função de iniciar a matriz, recebe o arquivo de pistas

# Substituir o valor da matriz pelos valores recebendo em algum momento aqui

def saida_grade(matriz):
    cont = 0
    for i in range(21):
        if lista_de_impres[i] < 3:
            print(saida[lista_de_impres[i]])
        else:
            print(f"{cont + 1}||{matriz[cont][0]}|{matriz[cont][1]}|{matriz[cont][2]}||{matriz[cont][3]}|{matriz[cont][4]}|{matriz[cont][5]}||{matriz[cont][6]}|{matriz[cont][7]}|{matriz[cont][8]}||{cont + 1}")
            cont += 1

# Função para verificar se o jogo está valido, recebe a matriz

matriz = [["   " for l in range(9)] for l in range(9)]
matriz[5][5] = " 7 "
saida_grade(matriz)
print(matriz)
