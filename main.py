# TRABALHO De FuP - SUDOKU
# Eric Rodrigues Gomes - 564971
# João Ítalo de Almeida Campos - 567991
# Marcos Vinicius Pereira Araujo - 571042 

import sys

from Classe import Sudoku
from validacao import validar_entrada, formatar, verificar_jogada, exibir_erro


# Função principal
def iniciar(modo):
    sudoku = Sudoku()

    modos = {
        1: executar_interativo,
        2: executar_batch
    }
    
    if modo in modos and not sudoku.finalizado:
        modos[modo](sudoku)

# função para executar o metodo interativo
def executar_interativo(sudoku):
    pistas_arquivo = obter_arquivo(1)
    registrar_acoes(sudoku, pistas_arquivo, True)

    sudoku.exibir_grade()
    if len(pistas_arquivo) < 1 or len(pistas_arquivo) > 80:
        sudoku.finalizado = True
        print("Configuracao de dicas invalida")
    while not sudoku.finalizado:
        acao = input("Insira sua ação: ")
        jogada = validar_entrada(sudoku, acao)
        
        if jogada != None and len(jogada) == 3: 
          registrar_acao(sudoku, jogada)
          sudoku.exibir_grade()
        elif jogada != None:
            exibir_erro(jogada[0], acao)
    print("Parabens!! jogo finalizado com sucesso")


# função para executar o metodo batch
def executar_batch(sudoku):
    global batch
    batch = True    
    
    # Receber o arquivo de pistas na forma de lista e de string formatada
    pistas_arquivo = obter_arquivo(1)
    pistas_str = obter_arquivo_str(1).replace(" ", "").replace('\r', '').replace('\n', '').strip().upper()

    # Validações específicas do batch
    invalida = False
    if len(pistas_arquivo) < 1 or len(pistas_arquivo) > 80:
        invalida = True
    for pista1 in pistas_arquivo:
        # Para cada pista na lista: formatar e então separar a pista entre coordenadas e numero da jogada
        pista1 = pista1.replace(" ", "").replace('\r', '').replace('\n', '').strip().upper().split(":")
        if pistas_str.count(pista1[0]) > 1:
            # Usando o arquivo na forma de string para checar se existem duas pistas para a mesma coordenada
            # Se existir mais de uma pista com a mesma coordenada, checar se algum desses casos declara numeros diferentes para a mesma coordenada
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


# função para o recebimento de arquivo
def obter_arquivo(i):
  with open(sys.argv[i], 'r') as file:
    return file.readlines()
def obter_arquivo_str(i):
    with open(sys.argv[i], 'r') as file:
        return file.read()

# função para registar um conjunto de ações (pistas ou o modo batch)
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
                else:
                    print('Configuracao de dicas invalida.')        
            # Caso seja batch fazer a formatação especifíca que ele pediu:
            else:
                if jogada_validada != None and len(jogada_validada) == 3:
                    registrar_acao(sudoku, jogada_validada)
                else:
                    jogada_validada = formatar(jogada)
                    print('A jogada ('+chr(jogada_validada[0]+65)+','+str(jogada_validada[1]+1)+') = '+str(jogada_validada[2])+' eh invalida!')
           

# função para realizar uma ação 
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
  print("O numero de parametros enviados para executar o sudoku eh invalido.")
else:
    if sys.argv[1] == "interface":
        from interface import iniciar_interface
        iniciar_interface()
    else:
        modo = len(sys.argv) - 1
        iniciar(modo)
