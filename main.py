import sys

from Classe import Sudoku

sudoku = Sudoku()

# Registra as mensagens de erro baseado em um número correspondente.
# Alguns eventos envolvem a jogada/ação do usuário e podem ser passadas como parâmetro da função.
def exibir_erro(codigo, entrada=None):

    if entrada != None:
        entrada = entrada.replace("\n", "").strip()
    
    erros = {
        1: "a linha ou a coluna está fora do alcance",
        2: "Você não pode interagir com uma pista.",
        3: "Você não pode ver as possibilidades de uma posição já preenchida",
        4: "msg 4",
        5: "O número precisa ser de 1 a 9",
        6: f"A jogada {entrada} não é possível",
        7: f"A jogada {entrada} eh invalida",
        8: "O número inserido é inválido.",
        9: "Não existe nada para ser apagado na posição solicitada."
    }
    
    if abs(codigo) in erros:
        print(erros[codigo])

def obter_arquivo(i):
  with open(sys.argv[i], 'r') as file:
    return file.readlines()
def obter_arquivo_str(i):
    with open(sys.argv[i], 'r') as file:
        return file.read()

def registrar_acoes(sudoku, arquivo, arquivo_pista=False, batch = False):
    for jogada in arquivo:
        if not sudoku.finalizado:
            jogada_validada = validar_entrada(sudoku, jogada)
            
            if arquivo_pista and not batch:
                if jogada_validada != None and arquivo_pista and len(jogada_validada) == 3:
                    registrar_acao(sudoku, jogada_validada)
                    
                    coluna, linha = jogada_validada[0], jogada_validada[1]
                    sudoku.pistas[linha][coluna] = True
                else:
                    print("erro tipo " + str(jogada_validada[0]))
                    exibir_erro(jogada_validada[0], jogada)
                    sudoku.finalizado = True
            elif arquivo_pista and batch:
                if (jogada_validada != None and arquivo_pista) or jogada_validada[0] == 2 or jogada_validada[0] == 6:
                    if len(jogada_validada) == 3:
                        registrar_acao(sudoku, jogada_validada)
                        coluna, linha = jogada_validada[0], jogada_validada[1]
                        sudoku.pistas[linha][coluna] = True
            # Caso seja batch fazer a formatação especifíca que ele pediu:
            else:
                if jogada_validada != None and len(jogada_validada) == 3:
                    registrar_acao(sudoku, jogada_validada)
                else:
                    jogada_validada = formatar(jogada)
                    print('A jogada ('+chr(jogada_validada[0]+65)+','+str(jogada_validada[1]+1)+') = '+str(jogada_validada[2])+' eh invalida!')
           
# Função principal
def iniciar(modo):
    sudoku = Sudoku()

    modos = {
        1: executar_interativo,
        2: executar_batch
    }
    
    if modo in modos and not sudoku.finalizado:
        modos[modo](sudoku)

def executar_batch(sudoku):
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
    
    registrar_acoes(sudoku, pistas_arquivo, True, True)            
    if not invalida and not sudoku.finalizado:
        jogadas_arquivo = obter_arquivo(2)
        registrar_acoes(sudoku, jogadas_arquivo, False, True)
        if sudoku.finalizado:
            print('A grade foi preenchida com sucesso!')
        else:
            print('A grade nao foi preenchida!')
    else:
        print('Configuracao de dicas invalida.')

def executar_interativo(sudoku):
    pistas_arquivo = obter_arquivo(1)
    registrar_acoes(sudoku, pistas_arquivo, True)

    sudoku.exibir_grade()

    while not sudoku.finalizado:
        acao = input("Insira sua ação: ")
        jogada = validar_entrada(sudoku, acao)
        
        if jogada != None and len(jogada) == 3:
          registrar_acao(sudoku, jogada)
          sudoku.exibir_grade()
        elif jogada != None:
            exibir_erro(jogada[0], acao)
        if sudoku.celulas_preenchidas == 81:
            sudoku.finalizado = True

def validar_entrada(sudoku, entrada):
    if formatar(entrada) == None:
        exibir_erro(7, entrada)
        return None
    else:
        return verificar_jogada(sudoku, formatar(entrada))
      

def formatar(entrada):
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
            conteudo = int(conteudo)
        
        # permite a ordem da linha e coluna de qualquer forma 
        if not linha.isnumeric():
            linha, coluna = coluna, linha
        linha = int(linha) - 1
        coluna = ord(coluna) - 65
        
        if coluna < 0 or coluna > 25:
            return None
    except ValueError:
        return None
    
    return [coluna, linha, conteudo]


def verificar_jogada(sudoku, entrada_formatada):
    coluna, linha, conteudo = entrada_formatada

    jogada_dados = [coluna, linha, conteudo]
    
    if linha < 0 or linha > 8 or coluna < 0 or coluna > 8:
        jogada_dados = [1]
    elif sudoku.pistas[linha][coluna]:
        jogada_dados = [2]
    elif conteudo == '?' and sudoku.grade[linha][coluna] != 0:
        jogada_dados = [3]
    elif conteudo == '!' and sudoku.grade[linha][coluna] == 0:
        jogada_dados = [9]
    elif conteudo == "?" or conteudo == "!":
        return jogada_dados
    else:
        conteudo = int(conteudo)

        quadrante = coluna // 3 + 3 * (linha // 3)

        if conteudo < 0 or conteudo > 9:
            jogada_dados = [5]
        elif sudoku.existe_numero_presente("linha", linha, conteudo) or sudoku.existe_numero_presente("coluna", coluna, conteudo) or sudoku.existe_numero_presente("quadrante", quadrante, conteudo):
            jogada_dados = [6]
        
    return jogada_dados

def registrar_acao(sudoku, acao):
    coluna, linha, conteudo = acao

    acoes = {
        "!": sudoku.apagar_numero,
        "?": sudoku.obter_dica
    }

    try:
        # checa se é um número de 1-9
        if 1 <= int(conteudo) <= 9:
            sudoku.inserir_numero(coluna, linha, int(conteudo))
    # se não for um número, vai tentar procurar uma ação com o conteudo da variável
    except ValueError:
        if conteudo in acoes:
            acoes[conteudo](coluna, linha)

# Inicialização e entrada de dados
# Modos de jogo:
# 1. Interativo
# 2. Batch
if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("O número de parâmetros enviados para executar o sudoku é inválido.")
else:
    modo = len(sys.argv) - 1
    iniciar(modo)
