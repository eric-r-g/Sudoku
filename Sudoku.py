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

def registrar_acoes(arquivo, eh_arquivo_pistas):
    global finalizado
    for jogada in arquivo:
        if not finalizado:
            if not batch:
                jogada = form_e_verif_entrada(jogada)
            else:
                jogada = formatacao(jogada)

            if eh_arquivo_pistas and not batch:
                if jogada[0] >= 0:
                    registrar_acao(jogada)
                    coluna, linha = jogada[0], jogada[1]
                    eh_pista[linha][coluna] = True
                else:
                    exibir_erro((jogada[0]))
                    finalizado = True
            elif eh_arquivo_pistas and batch:
                # A verificação das pistas do batch é diferente então estão sendo feitas no próprio executar_batch
                verificacao = verificar_jogada(jogada)[0]
                if verificacao >= 0 or verificacao == -6 or verificacao == -2:
                    registrar_acao(jogada)
                    coluna, linha = jogada[0], jogada[1]
                    eh_pista[linha][coluna] = True
                else:
                    finalizado = True
            elif batch:
                if jogada[0] != -7 and verificar_jogada(jogada)[0] >= 0:
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
    
    registrar_acoes(pistas_arquivo, True)            
    if not invalida and not finalizado:
        jogadas_arquivo = obter_arquivo(2)
        registrar_acoes(jogadas_arquivo, False)
        if finalizado:
            print('A grade foi preenchida com sucesso!')
        else:
            print('A grade nao foi preenchida!')
    else:
        print('Configuracao de dicas invalida.')

def exibir_erro(codigo):
    erros = {
        -1: "msg 1",
        -2: "msg 2",
        -3: "msg 3",
        -4: "msg 4",
        -5: "msg 5",
        -6: "msg 6",
        -7: "msg 7"
    }
    
    if codigo in erros:
        print(erros[codigo])

def executar_interativo():
    global finalizado
    pistas_arquivo = obter_arquivo(1)
    registrar_acoes(pistas_arquivo, True)

    quantidade_pistas = len(pistas_arquivo)
    if quantidade_pistas < 1 or quantidade_pistas > 80:
        print('Número inválido de pistas')
        finalizado = True
    elif not finalizado:
       saida_grade(matriz)

    while not finalizado:
        jogada = form_e_verif_entrada(input("Insira sua ação: "))
        
        if jogada[0] >= 0:
          registrar_acao(jogada)
          saida_grade(matriz)
        else:
          exibir_erro((jogada[0]))

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
        substituir = input("Já há um número nessa posição, deseja substituir? (Digite sim caso queira): ").strip().upper()
        if substituir == "SIM":
            num_pres_linha[linha][num_anterior] = False
            num_pres_coluna[coluna][num_anterior] = False
            num_pres_quadrante[quadrante][num_anterior] = False
            
    if num_anterior == ' ' or substituir == "SIM" or batch:
        matriz[linha][coluna] = numero
        num_pres_linha[linha][numero - 1] = True
        num_pres_coluna[coluna][numero - 1] = True
        num_pres_quadrante[quadrante][numero - 1] = True

def form_e_verif_entrada(entr):
    entr = formatacao(entr)
    if entr[0] == -7:
        return entr
    else:
        return verificar_jogada(entr)

def formatacao(entrada):
    try:
        entrada = entrada.replace(" ","").strip().upper()
        if "?" in entrada:
            coluna, linha = entrada.replace("?","").split(",")
            conteudo = "?"
        elif "!" in entrada:
            coluna, linha = entrada.replace("!","").split(",")
            conteudo = "!"
        else:
            entrada, conteudo = entrada.split(":")
            coluna, linha = entrada.split(",")

        # permite a ordem da linha e coluna de qualquer forma 
        if not linha.isnumeric():
            linha, coluna = coluna, linha
        linha = int(linha) - 1
        coluna = ord(coluna) - 65

        if coluna < 0 or coluna > 25:
            return[-7]
    except ValueError:
        return[-7]
    return[coluna, linha, conteudo]

def verificar_jogada(entrada_div):
    coluna, linha, conteudo = entrada_div

    retorno = [coluna, linha, conteudo]
    
    if linha < 0 or linha > 8 or coluna < 0 or coluna > 8:
        retorno = [-1]
    elif eh_pista[linha][coluna]:
        retorno = [-2]
    elif conteudo == '?':
      if matriz[linha][coluna] != " ":
        retorno = [-3]
    elif conteudo == '!':
        if matriz[linha][coluna] == " ":
            retorno = [-4]
    else:
        conteudo = int(conteudo) - 1
        quadrante = coluna // 3 + 3 * (linha // 3)
        if conteudo < 0 or conteudo > 8:
            retorno = [-5]
        elif (num_pres_linha[linha][conteudo] or num_pres_coluna[coluna][conteudo] or num_pres_quadrante[quadrante][conteudo]):
            retorno = [-6]
    return retorno

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
