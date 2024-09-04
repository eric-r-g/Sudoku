# Função para receber a entrada e retornar o que for necessário
    # Aqui dentro vai ter a leitura do arquivo provavelmente, talvez seja interessante alguém para isso já que a função é complicada por si só

# Função de iniciar a matriz, recebe o arquivo de pistas

# Substituir o valor da matriz pelos valores recebendo em algum momento aqui

def saida_grade(mat):
    # Essa função recebe a matriz e retorna a grade do sudoku já pronta
    # As variáveis aqui usadas são: 
        # A mat (a matriz recebida),
        # fil_padrao (as fileiras que não são modificadas), 
        # impres (a ordem das fileiras que será impressa),
        # lin (indica qual das 9 linhas está sendo modificada)

    fil_padrao = [
    "    A   B   C    D   E   F    G   H   I",
    " ++---+---+---++---+---+---++---+---+---++",
    " ++===+===+===++===+===+===++===+===+===++"
    ]
    impres = [0, 1, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 2, 3, 1, 3, 1, 3, 1, 0]
    lin = 0
    for i in range(21):
        if impres[i] < 3:
            print(fil_padrao[impres[i]])
        else:
            print("{}|| {} | {} |".format(lin + 1,mat[lin][0],mat[lin][1]),end="")
            print(" {} || {} | {} |".format(mat[lin][2],mat[lin][3],mat[lin][4]), end="")
            print(" {} || {} | {} |".format(mat[lin][5],mat[lin][6],mat[lin][7]), end="")
            print(" {} || {}".format(mat[lin][8], lin + 1))
            lin += 1

# Função para verificar se o jogo está valido, recebe a matriz

matriz = [[" " for l in range(9)] for l in range(9)]
saida_grade(matriz)
