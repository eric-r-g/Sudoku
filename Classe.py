import sys

# Classe principal que inicializa a matriz e os dados do jogo.
class Sudoku:
    def __init__(self):
        self.grade = [[0 for _ in range(9)] for _ in range(9)]
        self.pistas = [[False for _ in range(9)] for _ in range(9)]
        self.finalizado = False
    
    # Função para inserir um número dentro da grade.
    def inserir_numero(self, coluna, linha, numero):
        numero_atual = self.grade[linha][coluna]

        if self.pistas[linha][coluna]:
            exibir_erro(2)
        elif numero_atual != 0:
            substituir = input("Já existe um número nessa posição. Deseja substituir? (Digite 'sim' para prosseguir): ").strip().lower()
            if substituir == "sim":
                self.grade[linha][coluna] = numero
            # Caso o usuário digite outra coisa, o código irá prosseguir normalmente.
        else:
            self.grade[linha][coluna] = numero

    # Função responsável por apagar um número da grade.
    def apagar_numero(self, coluna, linha, numero):
        if self.grade[linha][coluna] == 0:
            exibir_erro(9)
        elif self.pistas[linha][coluna]:
            exibir_erro(2)
        else:
            self.grade[linha][coluna] = 0

    def existe_numero_presente(self, local, i, numero):
        # Analisa em uma coluna ou linha.
        if local.lower() == "coluna":
            for linha in range(9):
                if self.grade[linha][i] == numero:
                    return True

            return False

        elif local.lower() == "quadrante":
            inicio_linha = (i // 3) * 3
            inicio_coluna = (i % 3) * 3

            for x in range(inicio_linha, inicio_linha + 3):
                for y in range(inicio_coluna, inicio_coluna + 3):
                    if (self.grade[x][y] == numero):
                        return True

            return False

        # Se não for um dos casos acima, assume que seja uma linha
        else:
            for coluna in range(9):
                if self.grade[i][coluna] == numero:
                    return True
            return False

    # Analisa as possíveis posições para uma posição específicas e retorna quais números são possíveis de inserir.
    def verificar_possibilidades(self, coluna, linha):
        numeros_possiveis = []
        quadrante = (coluna // 3) + 3 * (linha // 3)

        for i in range(1, 10):
            if not (self.existe_numero_presente("linha", linha, i) or
                    self.existe_numero_presente("coluna", coluna, i) or
                    self.existe_numero_presente("quadrante", quadrante, i)):
                     numeros_possiveis.append(i)
        
        return numeros_possiveis

    def obter_dica(self, coluna, linha):
        n_possiveis = self.verificar_possibilidades(coluna, linha)

        if len(n_possiveis) == 0:
            print("Não possui números possiveis para essa posição.")
        else:
            print("Número(s) possiveis: " + ', '.join(map(str, n_possiveis)))

    def exibir_grade(self):
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
                # Formata o zero para uma string no formato " "
                linha_exibida = [str(self.grade[lin][col]) if self.grade[lin][col] != 0 else " " for col in range(9)]
                print("{}|| {} | {} |".format(lin + 1, linha_exibida[0], linha_exibida[1]), end="")
                print(" {} || {} | {} |".format(linha_exibida[2], linha_exibida[3], linha_exibida[4]), end="")
                print(" {} || {} | {} |".format(linha_exibida[5], linha_exibida[6], linha_exibida[7]), end="")
                print(" {} || {}".format(linha_exibida[8], lin + 1))
                lin += 1

# Registra as mensagens de erro baseado em um número correspondente.
# Alguns eventos envolvem a jogada/ação do usuário e podem ser passadas como parâmetro da função.
def exibir_erro(codigo, entrada=None):

    if entrada != None:
        entrada = entrada.replace("\n", "").strip()

    erros = {
        1: "msg 1",
        2: "Você não pode interagir com uma pista.",
        3: "msg 3",
        4: "msg 4",
        5: "msg 5",
        6: f"A jogada {entrada} não é possível",
        7: "A jogada " + entrada + " eh invalida",
        8: "O número inserido é inválido.",
        9: "Não existe nada para ser apagado na posição solicitada."
    }
    
    if abs(codigo) in erros:
        print(erros[codigo])

def obter_arquivo(i):
  with open(sys.argv[i], 'r') as file:
    return file.readlines()

def registrar_acoes(sudoku, arquivo, arquivo_pista=False):
    for jogada in arquivo:
        if not sudoku.finalizado:
            jogada_validada = validar_entrada(sudoku, jogada)

            if jogada_validada != None and arquivo_pista and len(jogada_validada) == 3:
                registrar_acao(sudoku, jogada_validada)

                coluna, linha = jogada_validada[0], jogada_validada[1]
                sudoku.pistas[linha][coluna] = True
            else:
                print("erro tipo " + str(jogada_validada[0]))
                exibir_erro(jogada_validada[0], jogada)
                sudoku.finalizado = True
           
# Função principal
def iniciar(modo):
    sudoku = Sudoku()

    pistas_arquivo = obter_arquivo(1)
    registrar_acoes(sudoku, pistas_arquivo, True)
    	
    modos = {
        1: executar_interativo,
        2: executar_batch
    }
    
    if modo in modos and not sudoku.finalizado:
        modos[modo](sudoku)

def executar_batch(sudoku):
    jogadas_arquivo = obter_arquivo(2)
    registrar_acoes(jogadas_arquivo, False)

    sudoku.exibir_grade()

def executar_interativo(sudoku):
    sudoku.exibir_grade()

    while not sudoku.finalizado:
        acao = input("Insira sua ação: ")
        jogada = validar_entrada(sudoku, acao)
        
        if jogada != None and len(jogada) == 3:
          registrar_acao(sudoku, jogada)
          sudoku.exibir_grade()
        elif jogada != None:
            exibir_erro(jogada[0], acao)

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

    print(f"c: {[coluna, linha, conteudo]}")
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
