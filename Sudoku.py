# Vamos colocar aqui variaveis que possivelmente iremos usar por todo o código

# matriz é a matriz contendo todos os números do suduko
matriz = [[" " for l in range(9)] for l in range(9)]

# num_pres_xxxx são matrizes booleanas para indicar se um número do intervalo de 1 a 9 
# está presente respectivamente na linha, coluna ou quadrante indicado

num_pres_linha = [[False for l in range(9)] for l in range(9)]
num_pres_coluna = [[False for l in range(9)] for l in range(9)]
num_pres_quadrante = [[False for l in range(9)] for l in range(9)]

# e_pista indica quais números da matriz são pistas ou não
e_pista = [[False for l in range(9)] for l in range(9)]


def inserir(linha, coluna, numero):
    numero = int(numero)
    quadrante = coluna // 3 + 3 * (linha // 3)
    matriz[linha][coluna] = numero + 1
    num_pres_linha[linha][numero] = True
    num_pres_coluna[coluna][numero] = True
    num_pres_quadrante[coluna][numero] = True

# Função de iniciar a matriz, recebe o arquivo de pistas

def dividirEntrada(entrada):
  # Função que recebe a string de entrada e retornar um array com a coluna, linha e o numero respectivamente
  # Tudo que é retornado é string, o numero vai ser o simbolo da operação se a entrada for uma operação "especial"
  # Não é feita nenhuma verificação se os valores são válidos, se o usuário colocar linha 10 vai ser retornada linha 10 por exemplo 
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
      
  linha = int(linha) - 1
  coluna = ord(coluna) - 65  
  return [col, linha, numero]

# Substituir o valor da matriz pelos valores recebidos em algum momento aqui

def verificarEntrada(entrada_div):
    # Função que recebe a coluna, a linha e qual comando (podendo ser um número) será realizado e 
    # verifica se aquela funcionalidade é possivel ou não. Será analisado para
    # a função de inserir, de retirar e de ver possibilidades e, além disso
    # a função retorna qual erro foi. Erros possiveis:
        # -1 - sem erros
        # 0 - linha ou coluna fora do alcance
        # 1 - interação com pista
        # 2 - verificação de possibilidades em espaço já ocupado
        # 3 - remoção em um espaço em branco
        # 4 - inserção de numero fora dos limites 
        # 5 - inserção de numero já presente (que fere as regras)
        
    # É feito aqui o ajuste das variaveis coluna e linha (para inteiros)
    coluna, linha, numero = entrada_div

    # É verificado cada possivel erro se acontece (em ordem listada)
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
        # Feiro ajuste da variavel número somente agora
        numero = int(numero) - 1
        quandrante = coluna // 3 + 3 * (linha // 3)
        if numero < 0 or numero > 8:
            return [False, 4]
        elif num_pres_linha[linha][numero] or num_pres_coluna[coluna][numero] or num_pres_quadrante[quandrante][numero]:
            return [False, 5]
            
    # Caso a função chegue até aqui, quer dizer que não houve erro algum, portanto
    # a função deverá prosseguir normalmente
    return [True, -1]

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
