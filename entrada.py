import sys

finalizado = False
matriz = [[" " for l in range(9)] for l in range(9)]

num_pres_linha = [[False for l in range(9)] for l in range(9)]
num_pres_coluna = [[False for l in range(9)] for l in range(9)]
num_pres_quadrante = [[False for l in range(9)] for l in range(9)]
e_pista = [[False for l in range(9)] for l in range(9)]

# entrada de dados
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("O número de parâmetros enviados para executar o sudoku é inválido.")

# 1 -> interativo
# 2 -> batch
modo = len(sys.argv) - 1:
obter_entradas()

def obter_arquivo(i):
    with open(sys.argv[i], 'r') as file:
        return file.read()

def registrar_acoes(arquivo):
    for jogada in arquivo:
        registrar_acao(formatar_entrada(pista))   

def obter_entradas():
    pistas_arquivo = obter_arquivo(1)
    registrar_jogadas(arquivo)
    	
    if (modo == 1):
        while not finalizado:
            j = input("Insira a jogada: ")
            registrar_acao(formatar_entrada(j))
    else:
        jogadas_arquivo = obter_arquivo(2)
        registrar_acoes(jogadas_arquivo)
        

# acao é uma array
def registrar_acao(acao):
    

def formatar_entrada(entrada):
  entrada = entrada.replace(" ","").upper()

  if "?" in entrada:
    col, linha = entrada.replace("?","").split(",")
    numero = "?"
  elif "!" in entrada:
    col, linha = entrada.replace("!","").split(",")
    numero = "!"
  else:
    entrada, numero = entrada.split(":")
    col, linha = entrada.split(",")
  return [col, linha, numero]

def verificar_jogada(entrada_div):
    coluna, linha, numero = entrada_div[0], entrada_div[1], entrada_div[2]
    linha = int(linha) - 1
    if ord(coluna) >= 97 and ord(coluna) <= 122:
        coluna = ord(coluna) - 97
    else:
        coluna = ord(coluna) - 65

    if linha < 0 or linha > 8 or coluna < 0 or coluna > 8:
        return [False, 0]
    elif e_pista[linha][coluna]:
        return [False, 1]
    elif numero == '?':
        if matriz[linha][coluna] != " ":
            return [False, 2]
    elif numero == '!':
        if matriz[linha][coluna] == " ":
            return [False, 3]
    else:
        numero = int(numero) - 1
        quandrante = coluna // 3 + 3 * (linha // 3)
        if numero < 0 or numero > 8:
            return [False, 4]
        elif num_pres_linha[linha][numero] or num_pres_coluna[coluna][numero] or num_pres_quandrante[quandrante][numero]:
            return [False, 5]
    return [True, -1]

def saida_grade(mat):
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
