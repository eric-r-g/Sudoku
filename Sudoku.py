import sys

quantidade_preenchida = 0;
finalizado = False
matriz = [[" " for l in range(9)] for l in range(9)]

# num_pres_xxxx são matrizes booleanas para indicar se um número do intervalo de 1 a 9 
# está presente respectivamente na linha, coluna ou quadrante indicado

num_pres_linha = [[False for l in range(9)] for l in range(9)]
num_pres_coluna = [[False for l in range(9)] for l in range(9)]
num_pres_quadrante = [[False for l in range(9)] for l in range(9)]

eh_pista = [[False for l in range(9)] for l in range(9)]

# entrada de dados
if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("O número de parâmetros enviados para executar o sudoku é inválido.")

# 1 -> interativo
# 2 -> batch
modo = len(sys.argv) - 1

def obter_arquivo(i):
  with open(sys.argv[i], 'r') as file:
    return file.readlines()

def registrar_acoes(arquivo, eh_arquivo_pistas):
  for jogada in arquivo:
    jogada = formatar_entrada(jogada)
    jogada_valida = verificar_jogada(jogada)
    if jogada_valida[0]:
      registrar_acao(jogada)
      if eh_arquivo_pistas:
        coluna, linha = jogada[0], jogada[1]
        eh_pista[linha][coluna] = True
    
       
# NOTA: essa meio que tá sendo a função principal, talvez vale mudar o nome ou dividir mais?
def obter_entradas():
    pistas_arquivo = obter_arquivo(1)
    registrar_acoes(pistas_arquivo, True)
    	
    if (modo == 1):
      saida_grade(matriz)
      while not finalizado:
        j = formatar_entrada(input("Insira a jogada: "))
        jogada_valida = verificar_jogada(j)
        if jogada_valida[0]:
          registrar_acao(j)
          saida_grade(matriz)
        else:
          # colocar aqui para imprimir os tipos de erro
          print('')
        if quantidade_preenchida = 81:
          finalizado = True
    else:
      jogadas_arquivo = obter_arquivo(2)
      registrar_acoes(jogadas_arquivo, False)
      saida_grade(matriz)

def apagar_numero(coluna, linha):
    numero = matriz[linha][coluna]
    quadrante = coluna // 3 + 3 * (linha // 3)
    matriz[linha][coluna] = " "
    num_pres_linha[linha][numero - 1] = False
    num_pres_coluna[coluna][numero - 1] = False
    num_pres_quadrante[quadrante][numero - 1] = False
    quantidade_preenchida -= 1

def numero_verificar_possibilidades(coluna, linha):
    quadrante = coluna // 3 + 3 * (linha // 3)
    saida = ""
    quantia = 0
    for i in range(9):
        if not num_pres_linha[linha][i] and not num_pres_coluna[coluna][i] and not num_pres_quadrante[quadrante][i]:
            quantia += 1
            if quantia != 1:
                saida = saida + ', '
            saida = saida + str(i + 1)
    return [saida, quantia] 
        
def registrar_acao(acao):
    coluna, linha, numero = acao
    if numero == "!":
        apagar_numero(coluna, linha)
    elif numero == "?":
        numeros_possiv, quant = verificar_possibilidades(coluna, linha)
        if quant == 0:
          print("não possui números possiveis")
        else:
          print("Número(s) possiveis: " +numeros_possiv)
    else:
        numero = int(numero)
        quadrante = coluna // 3 + 3 * (linha // 3)
        matriz[linha][coluna] = numero
        num_pres_linha[linha][numero - 1] = True
        num_pres_coluna[coluna][numero - 1] = True
        # NOTA: isso aqui> vvvvvvvvv <tava como "coluna" imagino que era pra ser quadrante e mudei 
        num_pres_quadrante[quadrante][numero - 1] = True
        quantidade_preenchida += 1

def formatar_entrada(entrada):
  entrada = entrada.replace(" ","").upper()

  if "?" in entrada:
    coluna, linha = entrada.replace("?","").split(",")
    numero = "?"
  elif "!" in entrada:
    coluna, linha = entrada.replace("!","").split(",")
    numero = "!"
  else:
    entrada, numero = entrada.split(":")
    coluna, linha = entrada.split(",")
  
  linha = int(linha) - 1
  coluna = ord(coluna) - 65
  return [coluna, linha, numero]

def verificar_jogada(entrada_div):
  coluna, linha, numero = entrada_div

  if linha < 0 or linha > 8 or coluna < 0 or coluna > 8:
    return [False, 0]
  elif eh_pista[linha][coluna]:
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
    elif num_pres_linha[linha][numero] or num_pres_coluna[coluna][numero] or num_pres_quadrante[quandrante][numero]:
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

obter_entradas()
