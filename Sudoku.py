import sys

finalizado = False
batch = False

# num_pres_xxxx são matrizes booleanas para indicar se um número do intervalo de 1 a 9 
# está presente respectivamente na linha, coluna ou quadrante indicado

matriz = [[" " for l in range(9)] for l in range(9)]
num_pres_linha = [[False for l in range(9)] for l in range(9)]
num_pres_coluna = [[False for l in range(9)] for l in range(9)]
num_pres_quadrante = [[False for l in range(9)] for l in range(9)]
eh_pista = [[False for l in range(9)] for l in range(9)]

def obter_arquivo(i):
  with open(sys.argv[i], 'r') as file:
    return file.readlines()
def obter_arquivo_str(i):
    with open(sys.argv[i], 'r') as file:
        return file.read()

def registrar_acoes(arquivo, eh_arquivo_pistas, batch = False):
    global finalizado
    for jogada in arquivo:
        if not finalizado:
            jogada = formatar_entrada(jogada)

            if eh_arquivo_pistas and not batch:
                if verificar_jogada(jogada)[0]:
                    registrar_acao(jogada)
                    coluna, linha = jogada[0], jogada[1]
                    eh_pista[linha][coluna] = True
                else:
                    exibir_erro(verificar_jogada(jogada)[1])
                    finalizado = True
            elif eh_arquivo_pistas:
                # A verificação das pistas do batch é diferente então estão sendo feitas no próprio executar_batch
                registrar_acao(jogada)
                coluna, linha = jogada[0], jogada[1]
                eh_pista[linha][coluna] = True
            elif batch:
                if verificar_jogada(jogada)[0]:
                    registrar_acao(jogada)
                else:
                    print('A jogada ('+chr(jogada[0]+65)+','+str(jogada[1]+1)+') = '+str(jogada[2])+' eh invalida!')
           
# Função principal
def iniciar(modo):
    	
    modos = {
        1: executar_interativo,
        2: executar_batch
    }
    
    if modo in modos and not finalizado:
        modos[modo]()

def executar_batch():
    # Solução talvez temporária pra um problema bem especifico:
    # Lá no inserir arquivo o miguel pede pra não perguntar se quer substituir caso seja batch
    global batch
    batch = True    

    pistas_arquivo = obter_arquivo(1)
    pistas_str = obter_arquivo_str(1).replace(" ", "").strip().upper()

    invalida = False
    if len(pistas_arquivo) < 1 or len(pistas_arquivo) > 80:
        invalida = True 
    for pista1 in pistas_arquivo:
        pista1 = pista1.replace(" ", "").strip().upper().split(":")
        if pistas_str.count(pista1[0]) > 1:
            for pista2 in pistas_arquivo:
                pista2  = pista2.replace(" ", "").strip().upper().split(":")
                if pista1[0] == pista2[0] and pista1[1] != pista2[1]: 
                    invalida = True
                
    if not invalida:
        registrar_acoes(pistas_arquivo, True, True)
        jogadas_arquivo = obter_arquivo(2)
        registrar_acoes(jogadas_arquivo, False, True)
        if finalizado:
            print('A grade foi preenchida com sucesso!')
        else:
            print('A grade nao foi preenchida!')
    else:
        print('Configuracao de dicas invalida.')

def exibir_erro(codigo):
    erros = {
        0: "msg 1",
        1: "msg 2",
        2: "msg 3",
        3: "msg 4",
        4: "msg 5",
        5: "msg 6"
    }
    
    if codigo in erros:
        print(erros[codigo])

def executar_interativo():
    pistas_arquivo = obter_arquivo(1)
    registrar_acoes(pistas_arquivo, True)

    saida_grade(matriz)

    quantidade_pistas = len(pistas_arquivo)
    if quantidade_pistas < 1 or quantidade_pistas > 80:
        print('Número inválido de pistas: '+quantidade_pistas)
        finalizado = True

    while not finalizado:
        j = formatar_entrada(input("Insira sua ação: "))
        jogada_valida = verificar_jogada(j)
        
        if jogada_valida[0]:
          registrar_acao(j)
          saida_grade(matriz)
        else:
          exibir_erro(jogada_valida[1])

def apagar_numero(coluna, linha):
    numero = matriz[linha][coluna]

    try:
        numero = int(numero)
        quadrante = coluna // 3 + 3 * (linha // 3)
        matriz[linha][coluna] = " "
        num_pres_linha[linha][numero - 1] = False
        num_pres_coluna[coluna][numero - 1] = False
        num_pres_quadrante[quadrante][numero - 1] = False
    # se não for um número, vai entender que a entrada n existe
    except ValueError:
        print("nao da pra apagar o nada paizao")

def verificar_possibilidades(coluna, linha):
    quadrante = coluna // 3 + 3 * (linha // 3)
    numeros_possiveis = []
    
    for i in range(9):
        if (not num_pres_linha[linha][i]
        and not num_pres_coluna[coluna][i]
        and not num_pres_quadrante[quadrante][i]):
            numeros_possiveis.append(i + 1)

    return numeros_possiveis

def obter_dica(coluna, linha):
    n_possiveis = verificar_possibilidades(coluna, linha)

    if len(n_possiveis) == 0:
        print("Não possui números possiveis para essa posição.")
    else:
        print("Número(s) possiveis: " + ', '.join(map(str, n_possiveis)))

def inserir_numero(coluna, linha, numero):
    
    substituir = ""
    num_anterior = matriz[linha][coluna]
    quadrante = coluna // 3 + 3 * (linha // 3)
    if num_anterior != ' ' and not batch:
        num_anterior = int(num_anterior) - 1
        substituir = input("Já há um número nessa posição, deseja substituir? (Digite sim caso queira): ").upper()
        if substituir == "SIM":
            num_pres_linha[linha][num_anterior] = False
            num_pres_coluna[coluna][num_anterior] = False
            num_pres_quadrante[quadrante][num_anterior] = False
            
    if num_anterior == ' ' or substituir == "SIM" or batch:
        matriz[linha][coluna] = numero
        num_pres_linha[linha][numero - 1] = True
        num_pres_coluna[coluna][numero - 1] = True
        num_pres_quadrante[quadrante][numero - 1] = True

def formatar_entrada(entrada):
  entrada = entrada.replace(" ","").strip().upper()

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
    coluna, linha, conteudo = entrada_div

    valida = [True]
    
    if linha < 0 or linha > 8 or coluna < 0 or coluna > 8:
        valida = [False, 0]
    elif eh_pista[linha][coluna]:
        valida = [False, 1]
    elif conteudo == '?':
      if matriz[linha][coluna] != " ":
        valida = [False, 2]
    elif conteudo == '!':
        if matriz[linha][coluna] == " ":
            valida = [False, 3]
    else:
        try:
            conteudo = int(conteudo) - 1
            quadrante = coluna // 3 + 3 * (linha // 3)
            if conteudo < 0 or conteudo > 8:
                valida = [False, 4]
            elif num_pres_linha[linha][conteudo] or num_pres_coluna[coluna][conteudo] or num_pres_quadrante[quadrante][conteudo]:
                valida = [False, 5]
        except ValueError:
            return valida
    
    return valida

def registrar_acao(acao):
    coluna, linha, conteudo = acao

    acoes = {
        "!": apagar_numero,
        "?": obter_dica 
    }

    try:
        # checa se é um número de 1-9
        if len(conteudo) == 1 and 1 <= int(conteudo) <= 9:
            inserir_numero(coluna, linha, int(conteudo))
    # se não for um número, vai tentar procurar uma ação com o conteudo da variável
    except ValueError:
        if conteudo in acoes:
            acoes[conteudo](coluna, linha)

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

# entrada de dados
# 1 -> interativo
# 2 -> batch
if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("O número de parâmetros enviados para executar o sudoku é inválido.")
else:
    modo = len(sys.argv) - 1
    iniciar(modo)
